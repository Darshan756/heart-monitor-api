# patients/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user_account.models import CustomUser
from .models import Patient, PatientAdmission, PatientHeartRate, Device
from datetime import date

class PatientTests(APITestCase):
    def setUp(self):
        self.doctor = CustomUser.objects.create_user(
            email='doc@example.com',
            password='Doctor123!',
            first_name='Doc',
            last_name='Tor',
            phone_number='1111111111',
            user_role='docter',
            is_active=True
        )

        self.nurse = CustomUser.objects.create_user(
            email='nurse@example.com',
            password='Nurse123!',
            first_name='Nu',
            last_name='Rse',
            phone_number='2222222222',
            user_role='nurse',
            is_active=True
        )

        self.other_user = CustomUser.objects.create_user(
            email='other@example.com',
            password='Other123!',
            first_name='Other',
            last_name='User',
            phone_number='3333333333',
            user_role='administration_staff',
            is_active=True
        )

        self.device1 = Device.objects.create(serial_number='DVC001', model_name='Heart Monitor X')
        self.device2 = Device.objects.create(serial_number='DVC002', model_name='Heart Monitor Y')

        self.client = APIClient()
        self.client.force_authenticate(user=self.doctor)

        self.patient_url = reverse('patients-list')
        self.admission_url = reverse('admissions-list')
        self.heartrate_url = reverse('heartrates-list')

        self.patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "phone_number": "9998887776",
            "email": "john@example.com",
            "address_line_1": "Street 1",
            "address_line_2": "",
            "city": "Bengaluru",
            "state": "Karnataka",
            "country": "India"
        }

    def test_create_patient(self):
        """Can create a new patient"""
        response = self.client.post(self.patient_url, self.patient_data, format='json')
        if response.status_code != 201:
            print("Patient creation error:", response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.get(email='john@example.com')
        self.assertEqual(patient.first_name, 'John')

    def test_patient_admission_validation(self):
        """Patient cannot be admitted twice without discharge"""
        patient = Patient.objects.create(**self.patient_data)

        response1 = self.client.post(self.admission_url, {
            "patient": patient.id,
            "admission_date": "2025-09-19T00:00:00Z",
            "assigned_device": self.device1.id,
            "admitted_by": self.doctor.id
        }, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(self.admission_url, {
            "patient": patient.id,
            "admission_date": "2025-09-20T00:00:00Z",
            "assigned_device": self.device2.id,
            "admitted_by": self.doctor.id
        }, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This patient is already admitted', str(response2.data))

    def test_create_heart_rate_by_doctor_or_nurse(self):
        """Only doctor or nurse can add heart rate"""
        patient = Patient.objects.create(**self.patient_data)
        admission = PatientAdmission.objects.create(
            patient=patient,
            admission_date=date.today(),
            assigned_device=self.device1,
            admitted_by=self.doctor
        )

        response = self.client.post(self.heartrate_url, {
            "patient": patient.id,
            "admission_detail": admission.id,
            "bpm": 80,
            "status": "normal",
            "notes": "Stable",
            "handled_by": self.doctor.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.other_user)
        response2 = self.client.post(self.heartrate_url, {
            "patient": patient.id,
            "admission_detail": admission.id,
            "bpm": 85,
            "status": "normal",
            "notes": "Stable",
            "handled_by": self.other_user.id
        }, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('not allowed to input heart rate', str(response2.data).lower())

    def test_search_patient_by_first_name(self):
        """Can search patients"""
        Patient.objects.create(**self.patient_data)
        response = self.client.get(self.patient_url + '?search=John')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['first_name'], 'John')
