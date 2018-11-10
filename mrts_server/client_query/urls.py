from django.urls import path
from . import views

urlpatterns = [
    path('route',views.client_query),
    path('stations/',views.list_stations),
]
