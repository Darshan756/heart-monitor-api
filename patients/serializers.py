from rest_framework import serializers
from .models import Patient, PatientAdmission, PatientHeartRate

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name','gender','date_of_birth', 'phone_number',
            'email', 'address_line_1', 'address_line_2', 'city', 'state', 'country'
        ]
        read_only_fields = ['id']

class PatientAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAdmission
        fields = ['id', 'patient', 'admission_date', 'assigned_device', 'discharge_date', 'admitted_by']
        read_only_fields = ['id']

    def validate(self, attrs):
        patient = attrs.get('patient')
        if PatientAdmission.objects.filter(patient=patient, is_discharge=False).exists():
            raise serializers.ValidationError('This patient is already admitted')
        return attrs


class PatientHeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHeartRate
        fields = ['patient', 'admission_detail', 'bpm', 'status', 'notes', 'handled_by']

    def validate(self, attrs):
        user = attrs.get('handled_by')
        if user.user_role not in ['docter', 'nurse']:
            raise serializers.ValidationError('You are not allowed to input heart rate')
        return attrs
