from django.db import models

# Create your models here.
class Phone(models.Model):
    userip = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    mobile = models.IntegerField()
