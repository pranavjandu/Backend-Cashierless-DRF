from django.shortcuts import render

from apps.users.serializers import *
from apps.users.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomerListView(APIView):
    """
    A class based view for creating and fetching customer records
    """

    def get(self, format=None):
        """
        Get all the customer records
        :param format: Format of the customer records to return to
        :return: Returns a list of customer records
        """
        customers = User.objects.all()
        serializer = UserSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a customer record
        :param format: Format of the customer records to return to
        :param request: Request object for creating customer
        :return: Returns a customer record
        """
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    def get(self, request, id, format=None):
        """
        Get the customer record for given id
        :param format: Format of the customer records to return to
        :return: Returns a list of customer records
        """
        try:
            customer = User.objects.get(id=id)
        except:
            error = {'error': 'Customer with given id not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
