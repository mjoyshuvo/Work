from rest_framework import serializers, viewsets
from apps.youtube.models import Channel, Video
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.api.Pagination import LargeResultsSetPagination


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = []


# Create your views here.


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class VideoViewSet(BaseViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    # permission_classes = [DjangoModelPermissions]
    serializer_class = VideoSerializer
    pagination_class = LargeResultsSetPagination
    # pagination_class = LimitOffsetPagination
    model = Video
    queryset = Video.objects.all()
    search_fields = ('name', 'tags', 'view_count')
    ordering_fields = ('name', 'tags', 'view_count')

    def get_queryset(self):
        queryset = Video.objects.all().order_by('id')
        tags = self.request.query_params.get('tags')
        """ Filter with Tags """
        # EX: http://127.0.0.1:8000/api/v1/youtube/videos/?tags=post malone, posty
        if tags:
            tags = tags.split(", ")
            queryset = Video.objects.filter(tags__contains=[tags])
        return queryset
