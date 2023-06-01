from django.db import models

class StringModel(models.Model):
    str_field = models.CharField(max_length=255)

class PhotoModel(models.Model):
    image = models.ImageField(upload_to='photos/')