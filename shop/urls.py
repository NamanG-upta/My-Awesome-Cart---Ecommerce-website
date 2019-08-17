from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="shophome"),
    path("about/", views.about, name="AboutUs"),
    path("search/", views.search, name="Search"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="tracker"),
    path("product/<int:myid>", views.productview, name="Productview"),
    path("checkout/", views.checkout, name="checkout"),
    path("handlerequest/", views.handlerequest, name="handlerequest")
]