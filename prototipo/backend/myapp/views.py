from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StringSerializer, PhotoSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class SomaView(APIView):
    def post(self, request):
        var_1 = int(request.data.get('var_1'))
        var_2 = int(request.data.get('var_2'))
        res = var_1 + var_2
        return Response({'resultado': res})

class StringView(APIView):
    def post(self, request):
        serializer = StringSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PhotoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)