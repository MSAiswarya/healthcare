from django.db import models
from django.contrib.auth.models import User

# UserProfile model for user roles
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Patient')  # Added missing role field
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"

# Patient model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="patient")  # Fixed user field
    phone = models.CharField(max_length=20, verbose_name="Phone Number", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

# Doctor model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Doctor",null=True,blank=True )
    # full_name=models.CharField(max_length=100,null=True,blank=True)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone Number")
    clinic_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

# Appointment model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient,related_name='appointments_as_doctor',on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,related_name='appointments_as_patient',on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.date} at {self.time}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
