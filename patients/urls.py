from rest_framework import routers
from django.urls import path,include
from .views import PatientViewSet,PatientAdmissionViewSet,PatientHeartRateViewSet
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'patients',PatientViewSet)
router.register(r'admissions',PatientAdmissionViewSet)
router.register(r'heartrates',PatientHeartRateViewSet)

urlpatterns = [
    path('',include(router.urls))
]
