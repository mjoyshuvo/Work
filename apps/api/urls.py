from django.conf.urls import url, include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from apps.user.views import ChangePasswordView

app_name = 'Api'

urlpatterns = [
    path('', include('apps.user.urls', 'user-api')),
    path('sales/', include('apps.sales.urls', 'sales-api')),
    path('common/', include('apps.common.urls', 'common-api')),
    path('parties/', include('apps.parties.urls', 'parites-api')),
    path('product_service/', include('apps.product_and_service.urls', 'product-service-api')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^change_password/', ChangePasswordView.as_view(), name='change_password'),
]
