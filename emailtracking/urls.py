from django.urls import path
from .views import startThreadView, stopThreadView

urlpatterns = [
    path('startthread', startThreadView, name='startthread'),
    path('stopthread', stopThreadView, name='stopthread'),
]