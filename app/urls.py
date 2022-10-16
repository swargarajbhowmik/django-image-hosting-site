from django.urls import path
from . import views

urlpatterns = [
    path("",views.IndexPage,name="index"),
    path("upload",views.UploadImage,name="upload"),
    path("view/<str:key>",views.ViewPage,name="viewpage"),
    path("key-deleted",views.KeyDeleted,name="key-deleted"),
    path("key-expired",views.KeyExpired,name="key-expired"),
    path("key-ip-mismatched",views.KeyIPMismatched,name="key-ip-mismatched"),
    path("verify",views.VerifyForTempPage,name="verify"),
    path("temp/<str:key>",views.ViewTempPage,name="temppage"),
    path("deletekey/<str:ik>",views.DeleteKey,name="deletekey"),
]