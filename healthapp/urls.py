from django.urls import path
#from .models import Appointment
from .import views
urlpatterns = [
    #Authenticaion related details
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.register,name='register'),
    path('profile/update/', views.update_profile, name='update_profile'),
    #Appointment realted Urls
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('appointments/view/<int:appointment_id>/', views.view_appointments, name='view_appointments'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/view/', views.view_appointments, name='view_appointments'),
    path('appointments/',views.appointment_list,name='appointments_list'),
    path('appointment/create/',views.create_appointment,name='create_appointment'),
    path('appointment/update/',views.update_appointment,name='update_appointment'),
    path('appointment/delete/',views.delete_appointment,name='delete_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'), 
    path('password_reset/', views.password_reset_done, name='password_reset'),
    path('password_reset/done/',views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/',views.password_reset_complete, name='password_reset_complete'),
    path('manage_doctors/', views.manage_doctors, name='manage_doctors'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_doctor/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),

    # Manage Patients
    path('manage_patients/', views.manage_patients, name='manage_patients'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('edit_patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<int:id>/', views.delete_patient, name='delete_patient'),
    #dashboard
    path('manage_doctors/', views.manage_doctors, name='manage_doctors'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),


    #Home URL
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact')
]
