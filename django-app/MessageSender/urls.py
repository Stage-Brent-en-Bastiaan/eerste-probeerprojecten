from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("patients/", views.getPatients, name="patients"),
    path("sendMessage/", views.getSendMessage, name="sendMessage"),
    path("filterData/", views.filterData, name="filterData"),
    path("postNewMessage/", views.postNewMessage, name="postNewMessage"),
]
