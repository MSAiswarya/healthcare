from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm,UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils import dateformat,timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Appointment, UserProfile
from .forms import AppointmentForm, UserRegistrationForm, LoginForm,UserProfileForm
from healthapp.models import Doctor, Patient
import logging
logger = logging.getLogger(__name__)
# Static pages
def home(request):
    return render(request, 'static_page/Home.html')

def about(request):
    return render(request, 'static_page/about.html')

def contact(request):
    return render(request, 'static_page/contact.html')

# Authentication views
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            elif user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid!")  # Debugging: Confirm form validation
            form.save()  # Save user to database
            print("User saved!")  # Debugging: Confirm user was saved
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to login page
        else:
            print("Form is invalid:", form.errors)  # Debugging: Output form errors
            messages.error(request, "There was an error in your registration form.")
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

# Password reset views
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Add proper email handling logic here
                    pass
                messages.success(request, "Password reset instructions sent to your email.")
                return redirect('login')
            else:
                messages.error(request, "No user is associated with this email address.")
    else:
        form = PasswordResetForm()
    return render(request, 'auth/password_reset.html', {'form': form})

def password_reset_done(request):
    return render(request, 'auth/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
    else:
        form = None

    return render(request, 'auth/password_reset_confirm.html', {'form': form})

def password_reset_complete(request):
    return render(request, 'auth/password_reset_complete.html')

# Dashboard views
@login_required
def doctor_dashboard(request):
    try:
        # Ensure the user is a doctor
        doctor = request.user.doctor
    except AttributeError:
        logger.error(f"No doctor profile found for user: {request.user.username}")
        return render(request, 'errors/error.html', {'message': 'No doctor profile found for this user.'})

    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient').order_by('date', 'time')
    print(appointments.query)
    # Pass the appointments to the template context
    context = {
        'user': request.user,
        'appointments':appointments
    }

    return render(request, 'dashboard/doctor_dashboard.html', context)
@login_required
def patient_dashboard(request):
    try:
        # Ensure the user is a patient
        patient = request.user.patient
    except AttributeError:
        logger.error(f"No patient profile found for user: {request.user.username}")
        return render(request, 'errors/error.html', {'message': 'No patient profile found for this user.'})

    upcoming_appointments = Appointment.objects.filter(patient=patient).select_related('doctor').order_by('date', 'time')

    # Pass the appointments to the template context
    context = {
        'user': request.user,
        'upcoming_appointments': upcoming_appointments
    }

    return render(request, 'dashboard/patient_dashboard.html', context) 
@login_required
def admin_dashboard(request):
    # Your logic for admin dashboard
    return render(request, 'dashboard/admin_dashboard.html')

def manage_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'dashboard/manage_doctors.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        # Process the form to add doctor
        pass
    return render(request, 'dashboard/add_doctor.html')

def edit_doctor(request, id):
    doctor = Doctor.objects.get(id=id)
    if request.method == 'POST':
        # Process the form to edit doctor
        pass
    return render(request, 'dashboard/edit_doctor.html', {'doctor': doctor})

def delete_doctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.delete()
    return redirect('manage_doctors')
def edit_appointment(request, appointment_id):
    # Get the appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Update the appointment details from the POST data
        appointment.patient.name = request.POST.get('patient_name')
        appointment.date = request.POST.get('appointment_date')
        appointment.time = request.POST.get('appointment_time')
        appointment.notes = request.POST.get('notes')

        # Save the changes to the database
        appointment.save()

        # Redirect to the doctor dashboard after saving
        return redirect('doctor_dashboard')

    # If it's GET request, render the form with current appointment details
# Manage Patients
def manage_patients(request):
    patients = Patient.objects.all()
    return render(request, 'dashboard/manage_patient.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        # Process the form to add patient
        pass
    return render(request, 'dashboard/add_patient.html')

def edit_patient(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        # Process the form to edit patient
        pass
    return render(request, 'dashboard/edit_patient.html', {'patient': patient})

def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.delete()
    return redirect('manage_patients')# Appointment views
@login_required
def view_appointments(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointments = Appointment.objects.all()
    return render(request, 'appointments/view_appointments.html', {'appointment': appointment})
def list_appointments(request):
    appointments = Appointment.objects.all()
    print("Appointments:", appointments)  
    return render(request, 'appointments/list_appointments.html', {'appointments': appointments})
@login_required
def appointment_list(request):
    if hasattr(request.user, 'profile'):
        role = request.user.profile.role
        if role == "Patient":
            appointments = Appointment.objects.filter(patient=request.user.profile.patient)
        elif role == "Doctor":
            appointments = Appointment.objects.filter(doctor=request.user.profile.doctor)
        else:
            appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.none()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})
@login_required
def my_appointments(request):
    # Get the logged-in user (patient)
    patient = request.user.patient

    # Get the appointments for this patient
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')

    # Pass appointments to the template
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard after saving
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'dashboard/update_profile.html', {'form': form})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            try:
                # Fetch the Patient instance associated with the logged-in user
                patient = Patient.objects.get(user=request.user)
                # Assign the Patient instance to the appointment
                appointment.patient = patient
                # Save the appointment
                appointment.save()
                return redirect('patient_dashboard')  # Redirect after saving the appointment
            except Patient.DoesNotExist:
                # Handle the case where there is no associated Patient
                return render(request, 'errors/error.html', {'message': 'No patient profile exists for the current user.'})
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})
@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.groups.filter(name="Doctors").exists() and appointment.doctor != request.user.profile.doctor:
        return HttpResponseForbidden("You cannot update this appointment")

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments/appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/update_appointment.html', {'form': form})

@login_required
def delete_appointment(request, appointment_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can delete appointments")
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointments/appointment_list')
# Error handlers
def custom_404(request, exception):
    return render(request, 'errors/error.html', {'message': 'Page not found'})

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_500(request):
     return render(request, 'errors/error.html', {'message': 'Internal server error'})
def create_missing_profiles(request):
    # Create missing Doctor profiles
    for user in User.objects.filter(groups__name='Doctors'):
         if not hasattr(user, 'Doctor'): 
            Doctor.objects.create(user=user)

    # Create missing Patient profiles
    for user in User.objects.filter(groups__name='Patients'):
        if not hasattr(user, 'patient'):
           Patient.objects.get_or_create(user=user)

    # Redirect to some page
    return redirect('home')  # Replace 'home' with your desired URL nam