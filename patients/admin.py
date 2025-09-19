from django.contrib import admin
from .models import Device,Patient,PatientAdmission,PatientHeartRate
# Register your models here.
admin.site.register(Device)
admin.site.register(Patient)
admin.site.register(PatientAdmission)
admin.site.register(PatientHeartRate)
