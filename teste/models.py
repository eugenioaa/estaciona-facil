from django.db import models

# Create your models here.
class Ruas(models.Model):
    title = models.CharField(max_lenght=50)
    DESCRIPTION = models.TextField()