from django.urls import path, include
from .views import \
    ProblemViewSet, \
    RawDataViewset, \
    LastProblemViewSet, \
    RawGetMethod,\
    LiveDataViewset

from rest_framework import routers


router = routers.DefaultRouter()
router.register('problem',ProblemViewSet)
router.register('lastproblem',LastProblemViewSet)
router.register('', RawDataViewset)



urlpatterns = [
    path('livedata',LiveDataViewset.as_view()),
    path('rawdata',RawGetMethod.as_view()),
    path('',include(router.urls)),



    # path('',)
]
