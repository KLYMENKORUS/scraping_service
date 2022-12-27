from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.register_view, name='register'),
    path('update/', views.update_view, name='update'),
    path('delete/', views.delete_view, name='delete'),
    path('contact/', views.contact, name='contact'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),
    path('password/reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/<token>/', views.PasswordConfirm.as_view(), name='password_reset_confirm'),
]