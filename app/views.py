from ast import Pass
from django.shortcuts import render, redirect
from .models import *
import random
import string
import datetime
import time
import urllib.request, json
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256

# Create your views here.
def IndexPage(request):
    return render(request, 'app/index.html')


def UploadImage(request):
    PasswordProtectionStatus = request.POST['password_protection_status']
    images = request.FILES['images']

    Time = time.strftime("%dth %B, %Y")
    with urllib.request.urlopen("http://ip-api.com/json") as url:
        data = json.load(url)
        country = list(data.values())[1]

    SecureImageKey = ''.join(random.choices(string.ascii_lowercase+string.ascii_uppercase, k=32))
    SecureImagePath = "https://murmuring-savannah-03830.herokuapp.com/view/"+SecureImageKey

    if(PasswordProtectionStatus=="true-pass"):
        Password = request.POST['image_password']
        encPass = make_password(Password)
        Q = ImageList.objects.create(Images=images, ImageKey=SecureImageKey, PassWordProtected="True", Password=encPass, UploaderCountry=country, UploadingTime=Time)
        return render(request, 'app/index.html', {'msg': SecureImagePath})
    else:
        Q = ImageList.objects.create(Images=images,ImageKey=SecureImageKey, PassWordProtected="False", Password="", UploaderCountry=country, UploadingTime=Time)
        return render(request, 'app/index.html', {'msg': SecureImagePath})

def ViewPage(request, key):
    getKeyData = ImageList.objects.get(ImageKey=key)
    Images = str(getKeyData.Images)
    ImageKey = getKeyData.ImageKey
    PassWordProtected = getKeyData.PassWordProtected
    Password = getKeyData.Password
    UploaderCountry = getKeyData.UploaderCountry
    UploadingTime = getKeyData.UploadingTime
    fetcheddata = [Images, ImageKey, PassWordProtected, Password, UploaderCountry, UploadingTime]
    return render(request, 'app/view.html', {'rdata':fetcheddata})
    # except:
    #     return redirect('https://murmuring-savannah-03830.herokuapp.com/404')

def VerifyForTempPage(request):
    ImgKey = request.POST['image_key']
    Password = request.POST['image_password']
    try:
        requestForTempPage = ImageList.objects.get(ImageKey=ImgKey)
        passVerify = django_pbkdf2_sha256.verify(Password, requestForTempPage.Password)
        if passVerify:
            ImageKey = str(requestForTempPage.ImageKey)
            Time = time.strftime("%d/%m/%Y %H:%M")
            SecureImageKey = ''.join(random.choices(string.ascii_lowercase+string.ascii_uppercase, k=32))
            with urllib.request.urlopen("http://ip-api.com/json") as url:
                data = json.load(url)
                ip = list(data.values())[13]
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            Q = TemporaryImageViewKeys.objects.create(ImageURL=ImageKey, ImageKey=SecureImageKey, IP=ip, RegisteredTime=current_time)
            generatedPrivateKey = 'https://murmuring-savannah-03830.herokuapp.com/temp/'+SecureImageKey
            return redirect(generatedPrivateKey)
        else:
            return redirect('https://murmuring-savannah-03830.herokuapp.com/wrong-pass')
    except:
        return redirect('https://murmuring-savannah-03830.herokuapp.com/404')

def ViewTempPage(request, key):
    try:
        requestForTempMedia = TemporaryImageViewKeys.objects.get(ImageKey=key)
        CurrentDate = datetime.datetime.now()
        CurrentDate = CurrentDate.strftime("%Y-%m-%d %H:%M:%S")
        ExpectedDate = requestForTempMedia.RegisteredTime
        ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%Y-%m-%d %H:%M:%S")
        threeHourLater = ExpectedDate + datetime.timedelta(hours = 6)
        ExpectedDate = datetime.datetime.strftime(threeHourLater , '%Y-%m-%d %H:%M:%S')
        ExpTime = ExpectedDate
        if ExpectedDate > CurrentDate:
            with urllib.request.urlopen("http://ip-api.com/json") as url:
                data = json.load(url)
                ip = list(data.values())[13]
            if requestForTempMedia.IP==ip:
                ViewKey = key
                ImageKey = requestForTempMedia.ImageURL
                getKeyData = ImageList.objects.get(ImageKey=ImageKey)
                Images = str(getKeyData.Images)
                ImageKey = getKeyData.ImageKey
                PassWordProtected = getKeyData.PassWordProtected
                Password = getKeyData.Password
                UploaderCountry = getKeyData.UploaderCountry
                UploadingTime = getKeyData.UploadingTime
                fetcheddata = [Images, ImageKey, PassWordProtected, Password, UploaderCountry, UploadingTime, ExpTime, ViewKey]
                return render(request, 'app/temp.html',{'rdata':fetcheddata})
            else:
                return redirect('https://murmuring-savannah-03830.herokuapp.com/key-ip-mismatched')
        else:
            return redirect('https://murmuring-savannah-03830.herokuapp.com/key-expired')
    except:
        return redirect('https://murmuring-savannah-03830.herokuapp.com/404')

def DeleteKey(request, ik):
    getdeletingData = TemporaryImageViewKeys.objects.get(ImageKey=ik)
    getdeletingData.delete()
    return redirect('/key-deleted')

def KeyDeleted(request):
    return render(request, 'app/key-deleted.html')

def KeyExpired(request):
    return render(request, 'app/key-expired.html')

def KeyIPMismatched(request):
    return render(request, 'app/key-ip-mismatched.html')