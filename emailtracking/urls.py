from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InboxViewSet, TicketViewSet, EmailIDViewSet, readMailView,ReportViewSet,DepartmentViewSet

router = DefaultRouter()
router.register('inbox', InboxViewSet)
router.register('ticket', TicketViewSet, basename='ticket')
router.register('email_ids', EmailIDViewSet)
router.register('reports', ReportViewSet)
router.register('departments', DepartmentViewSet)

urlpatterns = [
    path('readmail/', readMailView, name='read_mail'),
    path('', include(router.urls)),
]

