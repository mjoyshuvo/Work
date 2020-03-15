import operator
from functools import reduce
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.user.views import UserSerializer
from apps.api.Pagination import CustomResultsSetPagination


class CustomViewSetForQuerySet(viewsets.ModelViewSet):
    model = None
    change_keys = None
    search_keywords = None
    permission_id = None
    query = None

    def dt_search(self):
        search = self.request.query_params.get('filter', None)

        # search
        if search and search is not None and self.search_keywords is not None:
            search_logic = []

            for entity in self.search_keywords:
                search_logic.append(Q(**{entity + '__icontains': search}))

            self.query = self.query.filter(reduce(operator.or_, search_logic))

        return self.query

    # ascending or descending order
    def dt_order(self):
        column_id = self.request.query_params.get('order[0][column]', None)

        if column_id and column_id is not None:
            column_name = self.request.query_params.get(
                'columns[' + column_id + '][data]', None)

            if self.change_keys is not None:
                for key in self.change_keys:
                    if column_name == key:
                        column_name = self.change_keys.get(key)

            if column_name != '':
                order_dir = '-' if self.request.query_params.get(
                    'order[0][dir]') == 'desc' else ''
                self.query = self.query.order_by(order_dir + column_name)

        return self.query

    def get_queryset(self):
        if self.model is None:
            raise AssertionError('CustomViewSetForQuerySet need to include a model')

        self.query = self.model.objects.filter()
        self.query = self.dt_search()
        self.query = self.dt_order()
        return self.query

    # def get_permissions(self):
    #     if self.permission_id is None:
    #         raise AssertionError('CustomViewSetForQuerySet need to include a permission_id')
    #
    #     for permission in self.permission_classes:
    #         if permission.__name__ == 'GreenOfficeApiBasePermission':
    #             return [permission(self.permission_id)]
    #         else:
    #             return [permission()]


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomResultsSetPagination


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
