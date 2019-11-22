# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# app level imports
from .models import User
from .serializers import (
    UserLoginRequestSerializer,
    # UserVerifyRequestSerializer,
    # UserSerializer,
    UserRegSerializer,
    UserListSerializer,
    UserUpdateRequestSerializer
)

# project level imports
from libs.constants import (
        BAD_REQUEST,
        BAD_ACTION,
)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import ParseException
# from libs.helpers import time_it

# from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model  # If used custom user model
from django.contrib.auth import authenticate


class UserViewSet(GenericViewSet):
    """
    """
    queryset = User.objects.all()
    filter_backends = (filters.OrderingFilter,)
    authentication_classes = (TokenAuthentication,)

    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put']

    serializers_dict = {
        'login': UserLoginRequestSerializer,
        'register': UserRegSerializer,
        'list_exec': UserListSerializer,
        'exec': UserListSerializer,
        'exec_update': UserUpdateRequestSerializer,
        # 'list': UserListSerializer,
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False)
    def register(self, request):
        """
        """
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        print("registering user with", serializer.validated_data)

        user = serializer.create(serializer.validated_data)
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        """
        # old app hack
        try:
            int(request.META['HTTP_X_APP_VERSION'])
        except Exception as e:
            print(e)
            raise ParseException({"detail": "Please update to new version."})

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        print(serializer.validated_data)
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"])

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token = user.access_token
        return Response({'token': token},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):

        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        # url_path='image-upload',
        permission_classes=[IsAuthenticated, ],
    )
    def list_exec(self, request):
        """
        Return user profile data and groups
        """
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data, status.HTTP_200_OK)

    @action(
        methods=['get', 'patch'],
        detail=False,
        # url_path='image-upload',
        permission_classes=[IsAuthenticated, ],
    )
    def exec(self, request):
        """
        Return user profile data and groups
        """
        input_id = request.GET.get("id")
        try:
            d = User.objects.get(id=input_id)
            data = self.get_serializer(d).data
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

    @action(
        methods=['  '],
        detail=False,
        # url_path='image-upload',
        permission_classes=[IsAuthenticated, ],
    )
    def exec_update(self, request):
        """
        Return user profile data and groups
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise ParseException(BAD_REQUEST, serializer.errors)
        try:
            print(serializer.validated_data)
            d = User.objects.get(id="input_id")
            data = self.get_serializer(d).data
            return Response(data, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
