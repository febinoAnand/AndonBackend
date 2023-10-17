from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('button',ButtonViewSet)
router.register('indicator',IndicatorViewSet)
router.register('problem',ProblemCodeViewSet)
router.register('event',EventViewSet)
router.register('eventgroup',EventGroupViewSet)

urlpatterns =[
    path('',include(router.urls)),
]

