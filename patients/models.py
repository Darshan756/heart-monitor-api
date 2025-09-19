from django.db import models
import uuid
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class Device(models.Model):
    serial_number = models.CharField(unique=True,max_length=100)
    model_name    = models.CharField(max_length=100)
    manufacturer  = models.CharField(max_length=100,null=True,blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
         return f'{self.serial_number} {self.model_name}'
class Patient(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    first_name      = models.CharField(max_length=150)
    last_name       = models.CharField(max_length=150)
    date_of_birth   = models.DateField()
    phone_number    = models.CharField(max_length=15,unique=True)
    email           = models.EmailField(unique=True,null=True,blank=True)
    address_line_1  = models.CharField(max_length=200)
    address_line_2  = models.CharField(max_length=200)
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    country         = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
   
    def __str__(self):
        return self.get_full_name()
class PatientAdmission(models.Model):
    id               = models.UUIDField(default=uuid.uuid4,primary_key=True)
    patient          = models.ForeignKey(Patient,on_delete=models.CASCADE)
    assigned_device  = models.ForeignKey(Device,on_delete=models.CASCADE)
    admitted_by      = models.ForeignKey(User,on_delete=models.CASCADE)
    
    admission_date   = models.DateTimeField(auto_now_add=True)
    discharge_date   = models.DateTimeField(null=True,blank=True)

    is_discharge     = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-admission_date']
        verbose_name = 'PatientAdmission'
        verbose_name_plural = 'PatientAdmissions'
    def __str__(self):
        return f'{self.patient.get_full_name()} {self.admission_date}' 

    
class PatientHeartRate(models.Model):
    class StatusChoices(models.TextChoices):
            NORMAL = ('normal','Normal')
            HIGH   = ('high','High')
            LOW    = ('low','Low')
    id                   = models.UUIDField(default=uuid.uuid4,primary_key=True)
    patient              = models.ForeignKey(Patient,on_delete=models.CASCADE)
    admission_detail     = models.ForeignKey(PatientAdmission,on_delete=models.CASCADE)
    bpm            = models.PositiveIntegerField()
    status         = models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.NORMAL)
    notes          = models.TextField(null=True,blank=True)
    handled_by     = models.ForeignKey(User,on_delete=models.CASCADE)

    measured_at    = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-measured_at']

        verbose_name = 'HeartRate'
        verbose_name_plural = 'HeartRates'

    def __str__(self):
         return f'{self.patient.get_full_name()} {self.bpm} {self.status}'





    