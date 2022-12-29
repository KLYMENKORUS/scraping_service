from django.urls import path
from . import views


app_name = 'scraping'

urlpatterns = [
    path('list/vacancy/', views.VacancyList.as_view(), name='list_view'),
    path('detail/<int:pk>/vacancy/', views.VacancyDetail.as_view(), name='detail'),
    path('home/', views.home, name='home'),
]