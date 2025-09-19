from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.views import APIView
from .serializers import PatientSerializer,PatientAdmissionSerializer,PatientHeartRateSerializer
from .models import Patient,PatientAdmission,PatientHeartRate
from rest_framework.permissions import IsAuthenticated 
from user_account.authentication import CustomAuthentication
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer
    queryset= Patient.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['city','state','country']
    search_fields = ['first_name','last_name','email','phone_number']
    ordering_fields = ['date_of_birth']

class PatientAdmissionViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PatientAdmissionSerializer
    queryset=PatientAdmission.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['patient','discharge_date','admission_date']
    ordering_fields = ['admission_date']




class PatientHeartRateViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PatientHeartRateSerializer
    queryset=PatientHeartRate.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['status','handled_by']
    search_fields = ['patient__first_name', 'patient__last_name']

    ordering_fields = ['bpm']