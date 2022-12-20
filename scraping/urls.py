from django.urls import path
from . import views


app_name = 'scraping'

urlpatterns = [
    path('list/vacancy/', views.list_view, name='list_view'),
    path('home/', views.home, name='home'),
]