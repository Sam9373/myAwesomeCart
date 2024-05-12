from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStage"),
    path('search/', views.search, name="search"),
    path('productview/', views.productView, name="productview"),
    path('checkout/', views.checkout, name="checkout"),
]