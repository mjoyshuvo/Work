from rest_framework import serializers
from apps.api.views import BaseViewSet
from apps.product_and_service.models import ServiceItem, Service


class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = '__all__'


class ServiceItemViewSet(BaseViewSet):
    serializer_class = ServiceItemSerializer
    model = ServiceItem
    queryset = ServiceItem.objects.all()
    search_fields = ('name',)
    ordering_fields = ('name',)

    def get_queryset(self):
        item_type = self.request.query_params.get('type', None)
        if item_type:
            queryset = ServiceItem.objects.filter(type=item_type)
        else:
            queryset = ServiceItem.objects.all()

        return queryset


class ServiceSerializer(serializers.ModelSerializer):
    service_item_category_name = serializers.StringRelatedField(source='service_item_category.name')
    unit_type = serializers.StringRelatedField(source='get_unit_of_measurement_display')

    class Meta:
        model = Service
        fields = '__all__'


class ServiceViewSet(BaseViewSet):
    serializer_class = ServiceSerializer
    model = Service
    queryset = Service.objects.all()
    search_fields = ('name',)
    ordering_fields = ('name',)

