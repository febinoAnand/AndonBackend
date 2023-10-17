from django.urls import path, include
from .views import ProblemViewSet, RawDataViewset, LastProblemViewSet
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register('problem',ProblemViewSet)
router.register('', RawDataViewset)
# router.register('lastproblem',LastProblemViewSet)

urlpatterns = [
    path('',include(router.urls)),
    # path('',)
]
