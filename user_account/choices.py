from django.db import models 

class UserRole(models.TextChoices):
     ADMINISTARTION_STAFF = ('administration_staff','Administration_staff')
     DOCTER               = ('docter','Docter')
     NURSE                = ('nurse','Nurse')