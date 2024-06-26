from django.urls import path
from . import views

app_name = 'Baby_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
    path('stream/', views.livestream, name='livestream'),
    path('store_token/', views.store_token, name='store_token'),
    path('send/' , views.send, name="send"),
    path('publish/', views.publish_message, name='publish'),
    path('test-channels/<slug>/', views.async_dashboard, name='async_dashboard'),
]