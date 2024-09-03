from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('property-by-<str:property_city>/<str:property_city_id>/', views.get_hotel_by_city, name='property_by_city'),
    path('set_language/', views.set_language, name='set_language'),

    

]
