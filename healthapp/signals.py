# signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from healthapp.models import UserProfile, Doctor, Patient

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check the user's group to create the appropriate profile
        if instance.groups.filter(name='Doctors').exists():
            Doctor.objects.create(user=instance)
        elif instance.groups.filter(name='Patients').exists():
            Patient.objects.create(user=instance)
        else:
            UserProfile.objects.create(user=instance)  # Default profile

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the User is saved."""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='Patients').exists():  # Check if the user belongs to the "Patients" group
        Patient.objects.create(user=instance)