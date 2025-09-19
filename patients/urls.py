from rest_framework import routers
from django.urls import path,include
from .views import PatientViewSet,PatientAdmissionViewSet,PatientHeartRateViewSet
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'admissions', PatientAdmissionViewSet, basename='admissions')
router.register(r'heartrates', PatientHeartRateViewSet, basename='heartrates')


urlpatterns = [
    path('',include(router.urls))
]
