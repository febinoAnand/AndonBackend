from django.urls import path,include
from .views import *
from rest_framework import routers
from .views import GetButtonView, GetEventView, GetEventGroupView, GetIndicatorView, GetProblemCodeView,GetMachineEventView


router = routers.DefaultRouter()
router.register('button',ButtonViewSet)
router.register('indicator',IndicatorViewSet)
router.register('problem',ProblemCodeViewSet)
router.register('event',EventViewSet)
router.register('eventgroup',EventGroupViewSet)

urlpatterns =[
    path('',include(router.urls)),
    # path('getButtons',GetButtonView.as_view()),
    # path('getIndicator',GetIndicatorView.as_view()),
    # path('getProblemCode',GetProblemCodeView.as_view()),
    # path('getEvent',GetEventView.as_view()),
    # path('getEventGroup',GetEventGroupView.as_view()),
    path('getMachineEvents',GetMachineEventView.as_view()),

]

