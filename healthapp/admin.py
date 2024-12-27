from django.contrib import admin
# Register your models here.
from .models import Patient,Doctor,Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'doctor', 'patient', 'description')  # Ensure all fields exist
    list_filter = ('date', 'doctor')  # Use valid fields from the model
    ordering = ('date',)  # Use a valid field for ordering

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('specialization', 'phone', 'clinic_address')
    list_filter = ('specialization',)  # Use valid fields from the model
    ordering = ('user__first_name',)  # Use a valid field for ordering

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'birth_date')
    list_filter = ('birth_date',)  # Use valid fields from the model
    ordering = ('user__first_name',)  # Use a valid field for ordering

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)