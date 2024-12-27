from django import forms
from .models import Appointment, Patient, Doctor, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
# Appointment form
class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),  # Queryset to list all doctors
        empty_label="Select a Doctor",  # Optional placeholder
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['doctor','date', 'time', 'doctor', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    # Custom validation method for the date field
    def clean_date(self):
        # Access the cleaned data of the date field
        date = self.cleaned_data.get('date')
        
        # Perform validation to check if the date is in the past
        if date < timezone.now().date():
            raise forms.ValidationError("The date cannot be in the past!")
        
        # Return the cleaned date if validation passes
        return date
# User registration form
class UserRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

# Patient registration form
class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# Patient profile form
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'address', 'birth_date']

# Doctor registration form
class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# Doctor profile form
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone', 'clinic_address']

# Login form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Appointment search form
class AppointmentSearchForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False)

    class Meta:
        fields = ['date', 'doctor']
        error_messages = {
            'date': {
                'required': "Please select a valid date",
            },
        }
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role','bio', 'phone', 'address']  # Add the fields you need from UserProfile