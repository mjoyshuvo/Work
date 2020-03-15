from rest_framework import serializers
from apps.api.views import BaseViewSet
from apps.parties.models import Customers, CustomerCategory, Vendors, VendorCategory


class CustomerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCategory
        fields = '__all__'


class CustomerCategoryViewSet(BaseViewSet):
    serializer_class = CustomerCategorySerializer
    model = CustomerCategory
    queryset = CustomerCategory.objects.all()
    search_fields = ('name',)
    ordering_fields = ('name',)


class CustomersSerializer(serializers.ModelSerializer):
    relationship_name = serializers.StringRelatedField(source='get_relationship_display')
    bank_name = serializers.StringRelatedField(source='bank.name')
    category_name = serializers.StringRelatedField(source='category.name')
    sub_type_name = serializers.StringRelatedField(source='get_sub_type_display')

    class Meta:
        model = Customers
        fields = '__all__'


class CustomerViewSet(BaseViewSet):
    serializer_class = CustomersSerializer
    model = Customers
    queryset = Customers.objects.all()
    search_fields = ('name', 'sub_type')
    ordering_fields = ('name',)


class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = '__all__'


class VendorCategoryViewSet(BaseViewSet):
    serializer_class = VendorCategorySerializer
    model = VendorCategory
    queryset = VendorCategory.objects.all()
    search_fields = ('name',)
    ordering_fields = ('name',)


class VendorSerializer(serializers.ModelSerializer):
    relationship_name = serializers.StringRelatedField(source='get_relationship_display')
    bank_name = serializers.StringRelatedField(source='bank.name')
    category_name = serializers.StringRelatedField(source='category.name')
    sub_type_name = serializers.StringRelatedField(source='get_sub_type_display')

    class Meta:
        model = Vendors
        fields = '__all__'


class VendorViewSet(BaseViewSet):
    serializer_class = VendorSerializer
    model = Vendors
    queryset = Vendors.objects.all()
    search_fields = (
        'name', 'sub_type', 'opening_balance', 'code', 'pin_number', 'email', 'nationality', 'mobile',
        'founded_on', 'registration_no', 'vat_registration_no', 'relationship', 'account_name', 'account_number',
        'contact_person_name', 'contact_person_mobile', 'contact_person_email')
    ordering_fields = (
        'name', 'sub_type', 'opening_balance', 'code', 'pin_number', 'email', 'nationality', 'mobile',
        'founded_on', 'registration_no', 'vat_registration_no', 'relationship', 'account_name', 'account_number',
        'contact_person_name', 'contact_person_mobile', 'contact_person_email')
