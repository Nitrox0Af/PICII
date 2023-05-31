from rest_framework import serializers
from .models import StringModel, PhotoModel

class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringModel
        fields = {}

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoModel
        fields = {}