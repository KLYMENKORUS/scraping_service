from django.urls import path
from . import views


app_name = 'scraping'

urlpatterns = [
    path('home/', views.ListHomeView.as_view(), name='home'),
]