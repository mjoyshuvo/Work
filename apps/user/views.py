from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import DjangoModelPermissions
from apps.user.models import UserProfile, Role, Permission
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.api.Pagination import LargeResultsSetPagination, CustomResultsSetPagination
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = [DjangoModelPermissions]


# Create your views here.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password']

    def create(self, validated_data):
        # user = UserProfile.objects.create_user(**validated_data)
        # user.set_password()
        validated_data.update({'password': make_password(validated_data.get('password'))})
        user = UserProfile.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    permission_classes = []
    serializer_class = UserSerializer
    pagination_class = CustomResultsSetPagination
    model = UserProfile
    queryset = UserProfile.objects.all()
    search_fields = ('first_name', 'last_name')
    ordering_fields = ('first_name', 'last_name')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = UserProfile
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong old password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(default=True)
    permission_name = serializers.StringRelatedField(
        source='permission', many=True, read_only=True)
    user_count = serializers.StringRelatedField(
        source='user.count', read_only=True)

    class Meta:
        model = Role
        fields = '__all__'


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    pagination_class = LargeResultsSetPagination
    model = Role
    queryset = Role.objects.all()
