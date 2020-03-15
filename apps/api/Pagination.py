from collections import OrderedDict

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    limit_query_param = 'length'
    offset_query_param = 'start'
    max_limit = 100

    def get_paginated_response(self, data):
        try:
            draw = self.request.query_params.get('draw')
        except MultiValueDictKeyError:
            draw = 1

        return Response(OrderedDict([
            ('recordsTotal', self.count),
            ('recordsFiltered', self.count),
            ('draw', draw),
            ('data', data)
        ]))


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'per_page': self.page_size,
            "current_page": self.page.number,
            "last_page": self.page.paginator.num_pages,
            'next_page_url': self.get_next_link(),
            'prev_page_url': self.get_previous_link(),
            'from': self.page.start_index(),
            'to': self.page.end_index(),
            'data': data
        })


