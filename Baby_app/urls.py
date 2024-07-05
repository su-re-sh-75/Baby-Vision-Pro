from django.urls import path
from . import views

app_name = 'Baby_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/initial-data/', views.get_initial_data, name='initial-data'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
    path('stream/', views.livestream, name='livestream'),
    path('publish/', views.publish_message, name='publish'),
]