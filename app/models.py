from xml.dom.domreg import registered
from django.db import models

# Create your models here.
class ImageList(models.Model):
    Images = models.ImageField(upload_to="")
    ImageKey = models.CharField(max_length=255)
    PassWordProtected = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    UploaderCountry = models.CharField(max_length=255)
    UploadingTime = models.CharField(max_length=255)

class TemporaryImageViewKeys(models.Model):
    ImageURL = models.CharField(max_length=255)
    ImageKey = models.CharField(max_length=255)
    IP = models.CharField(max_length=255)
    RegisteredTime = models.CharField(max_length=255)