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
from .models import Client, Job

# project level imports
from libs.constants import (
        BAD_REQUEST,
        BAD_ACTION,
)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import ParseException
# from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model  # If used custom user model
# from django.contrib.auth import authenticate

from .serializers import (
    ClientCreateRequestSerializer,
    ClientListSerializer,
    JobCreateRequestSerializer,
    JobListSerializer
)


# class CreateUserView(CreateAPIView):
#     model = get_user_model()
#     permission_classes = [
#         permissions.AllowAny # Or anon users can't register
#     ]
#     serializer_class = UserRegSerializer


class ClientViewSet(GenericViewSet):
    """
    """
    queryset = Client.objects.all()
    filter_backends = (filters.OrderingFilter,)
    authentication_classes = (TokenAuthentication,)

    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put']

    serializers_dict = {
        'org': ClientCreateRequestSerializer,
        'org_details': ClientCreateRequestSerializer,
        'org_list': ClientListSerializer

    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
    def org(self, request):
        """
        """
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            print(serializer.errors)
            raise ParseException(BAD_REQUEST, serializer.errors)

        print("create client with", serializer.validated_data)

        client = serializer.create(serializer.validated_data)
        if client:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
    def org_details(self, request):
        """
        """
        client_id = request.GET.get("id")
        try:
            client_obj = Client.objects.get(id=client_id)
            client_data = self.get_serializer(client_obj).data
            print("client_data", client_data)
            return Response(client_data, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
    def org_list(self, request):
        """
        """
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data, status.HTTP_200_OK)

    # @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated, ],)
    # def org_details(self, request):
    #     """
    #     """
    #     serializer = self.get_serializer(data=request.data)

    #     if not serializer.is_valid():
    #         raise ParseException(BAD_REQUEST, serializer.errors)
    #     try:
    #         print(serializer.validated_data)
    #         d = Client.objects.get(id="input_id")
    #         data = self.get_serializer(d).data
    #         return Response(data, status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


class JobViewSet(GenericViewSet):
    """
    """
    queryset = Job.objects.all()
    filter_backends = (filters.OrderingFilter,)
    authentication_classes = (TokenAuthentication,)

    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put']

    serializers_dict = {
        'job': JobCreateRequestSerializer,
        'job_details': JobCreateRequestSerializer,
        'job_list': JobListSerializer,

    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
    def job(self, request):
        """
        """
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            print(serializer.errors)
            raise ParseException(BAD_REQUEST, serializer.errors)

        print("create job with", serializer.validated_data)

        job_obj = serializer.create(serializer.validated_data)
        if job_obj:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
    def job_details(self, request):
        """
        """
        job_id = request.GET.get("id")
        try:
            job_obj = Job.objects.get(id=job_id)
            job_data = self.get_serializer(job_obj).data
            print("job_data", job_data)
            return Response(job_data, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
    def job_list(self, request):
        """
        """
        org_id = request.GET.get("org_id")
        if not org_id:
            return Response({"status": "org_id Not Found"}, status.HTTP_404_NOT_FOUND)
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data, status.HTTP_200_OK)

    # @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated, ],)
    # def job_details(self, request):
    #     """
    #     """
    #     serializer = self.get_serializer(data=request.data)

    #     if not serializer.is_valid():
    #         raise ParseException(BAD_REQUEST, serializer.errors)
    #     try:
    #         print(serializer.validated_data)
    #         d = Client.objects.get(id="input_id")
    #         data = self.get_serializer(d).data
    #         return Response(data, status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
