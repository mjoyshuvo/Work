from rest_framework import serializers, viewsets
from apps.sales.models import DummyServicePurchased, Sales, SalesInvoice
from apps.api.Pagination import LargeResultsSetPagination
from apps.api.views import BaseViewSet
from django.db.models import Count
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Sum
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from conf.settings import APP_HOST, MEDIA_ROOT, MEDIA_URL
from django.http import HttpResponse
import os
import bangla
from datetime import datetime, timedelta
from apps.parties.models import Customers
from django.db import transaction
import json


class SupplierPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyServicePurchased
        fields = '__all__'


class SupplierPurchasedViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierPurchasedSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = []
    model = DummyServicePurchased
    queryset = DummyServicePurchased.objects.all()

    def list(self, request, *args, **kwargs):
        dummy_services = DummyServicePurchased.objects.all()
        print(dummy_services)
        sum_elements = dummy_services.aggregate(total_vat=Sum('vat_amount'),
                                                total_subsidiary_vat=Sum(
                                                    'subsidiary_vat'),
                                                total_price_before_vat=Sum('unit_total'),
                                                total_price_after_vat=Sum(
                                                    'price_after_vat'))

        data_content = render_to_string('mushok_template/Mushok 6.3(Tax Challan New).html', {
            'dummy_services': dummy_services,
            'total_vat': sum_elements['total_vat'],
            'total_subsidiary_vat': sum_elements['total_subsidiary_vat'],
            'total_price_before_vat': sum_elements['total_price_before_vat'],
            'total_price_after_vat': sum_elements['total_price_after_vat'],
            'bangla_converter': bangla.convert_english_digit_to_bangla_digit
        })
        pdf_file = HTML(string=data_content, base_url=APP_HOST).write_pdf(presentational_hints=True)
        # response = HttpResponse(pdf_file, content_type='application/pdf')
        # response['Content-Disposition'] = 'filename=Mushok 6.3(Tax Challan).pdf'
        file_name = 'output_mushok_copy/Mushok 6.3(Tax Challan).pdf'
        f = open(os.path.join(MEDIA_ROOT, file_name), 'wb')
        f.write(pdf_file)
        created_pdf_file = os.path.join(MEDIA_ROOT, file_name)
        if os.path.exists(created_pdf_file):
            return HttpResponse(self.request.build_absolute_uri(MEDIA_URL + file_name))
        else:
            return HttpResponse({'status': 'File Not Found'})


class SalesSerializer(serializers.ModelSerializer):
    service_name = serializers.StringRelatedField(source='service.name')
    customer_name = serializers.StringRelatedField(source='customer.name')
    unit_type = serializers.StringRelatedField(source='service.unit_of_measurement')

    class Meta:
        model = Sales
        fields = '__all__'

    def create(self, validated_data):
        # validated_data.update({'password': make_password(validated_data.get('password'))})
        service = validated_data.get('service')
        quantity = validated_data.get('quantity')
        per_unit_price = service.sell_price
        validated_data.update({'per_unit_price': per_unit_price})
        vat_per_unit = service.vat
        validated_data.update({'vat_per_unit': vat_per_unit})
        unit_total = per_unit_price * quantity
        validated_data.update({'unit_total': unit_total})
        vat_amount = (unit_total * vat_per_unit / 100)
        validated_data.update({'vat_amount': vat_amount})
        price_after_vat = unit_total + vat_amount
        validated_data.update({'price_after_vat': price_after_vat})
        sales_invoice = Sales.objects.create(**validated_data)
        return sales_invoice


class SalesViewSet(BaseViewSet):
    serializer_class = SalesSerializer
    model = Sales
    queryset = Sales.objects.all()

    def get_queryset(self):
        queryset = Sales.objects.all()
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            queryset = Sales.objects.filter(invoice_id=invoice_id)
        return queryset


class SalesInvoiceSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True)

    class Meta:
        model = SalesInvoice
        fields = '__all__'


class SalesInvoiceViewSet(BaseViewSet):
    serializer_class = SalesInvoiceSerializer
    model = SalesInvoice
    queryset = SalesInvoice.objects.all()

    def get_queryset(self):
        queryset = SalesInvoice.objects.all()
        is_approved = self.request.query_params.get('approved')
        perform_approve = self.request.query_params.get('perform_approve')
        if is_approved:
            queryset = SalesInvoice.objects.filter(approved=is_approved)
        # -------- Approve Invoice ----------
        if perform_approve:
            sales_invoice = SalesInvoice.objects.get(id=perform_approve)
            sales_invoice.approved = True
            sales_invoice.save()
            return SalesInvoice.objects.filter(approved=False)
        return queryset


"""Posts Sales Entry after creating Sales Invoice"""
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def service_invoice(request):
    with transaction.atomic():
        print(request.data)
        sales = request.data
        sales_invoice = SalesInvoice.objects.create()
        for sale in sales:
            Sales.objects.create(invoice_id=sales_invoice.id, service_id=sale['service'], customer_id=sale['customer'],
                                 quantity=sale['quantity'], per_unit_price=sale['sell_price'], unit_total=sale['amount'],
                                 vat_per_unit=sale['vat_p'], vat_amount=sale['vat'], price_after_vat=sale['payable'],
                                 order_date=sale['order_date'])
        return HttpResponse({'status': 'OK'})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def tax_challan_report(request):
    invoice_id = request.GET['invoice_id']
    if invoice_id:
        invoice_number = SalesInvoice.objects.get(id=invoice_id).invoice_number
        service_invoices = Sales.objects.filter(invoice_id=invoice_id)
        customers = service_invoices.values_list('customer', flat=True).distinct('customer')
        customer_list = []
        for customer in customers:
            customer_service_data = service_invoices.filter(customer=customer)
            data_slice = [customer_service_data[x:x + 25] for x in
                          range(0, len(customer_service_data), 25)]
            for chunk in range(len(data_slice)):
                customer_obj = Customers.objects.get(pk=customer)
                last_index = len(data_slice) - 1
                customer_data = {}
                customer_data['customer_info'] = {
                    'customer_name': customer_obj.name,
                    'customer_shipping_address': customer_obj.shipping_address,
                    'customer_invoice_number': invoice_number,
                    'customer_code': customer_obj.code,
                    'is_last': False,
                    'index': 0
                }
                if chunk != 0:
                    customer_data['customer_info']['index'] = customer_data['customer_info']['index'] + 25
                customer_data['customer_service_invoices'] = data_slice[chunk]
                customer_data['sum_element'] = customer_service_data.aggregate(total_vat=Sum('vat_amount'),
                                                                               total_subsidiary_vat=Sum(
                                                                                   'subsidiary_vat'),
                                                                               total_price_before_vat=Sum('unit_total'),
                                                                               total_price_after_vat=Sum(
                                                                                   'price_after_vat'))
                if chunk == last_index:
                    customer_data['customer_info']['is_last'] = True
                customer_list.append(customer_data)
        data_content = render_to_string('mushok_template/Mushok 6.3(Tax Challan New)_v3.html', {
            'customer_list': customer_list,
            'bangla_converter': bangla.convert_english_digit_to_bangla_digit,
            'issue_date': datetime.today().strftime("%Y-%m-%d"),
            'issue_date_time': (datetime.now() + timedelta(hours=6)).strftime("%b %d, %Y %I:%M:%S %p"),
            'time_bottom': (datetime.now() + timedelta(hours=6)).strftime("%d/%m/%Y %-I:%m")
        })
        pdf_file = HTML(string=data_content, base_url=APP_HOST).write_pdf(presentational_hints=True)
        # response = HttpResponse(pdf_file, content_type='application/pdf')
        # response['Content-Disposition'] = 'filename=Mushok 6.3(Tax Challan).pdf'
        file_name = 'output_mushok_copy/Mushok 6.3(Tax Challan).pdf'
        f = open(os.path.join(MEDIA_ROOT, file_name), 'wb')
        f.write(pdf_file)
        created_pdf_file = os.path.join(MEDIA_ROOT, file_name)
        if os.path.exists(created_pdf_file):
            print(request.build_absolute_uri(MEDIA_URL + file_name))
            return HttpResponse(request.build_absolute_uri(MEDIA_URL + file_name))
        else:
            return HttpResponse({'status': 'File Not Found'})
