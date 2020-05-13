"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from donation.views import LandingPage, AddDonation, Login, Register, FormConfirmationView, Logout, AdminPanel, \
    EditUser, DeleteUser, AddUser, ProfilUser, ArchiveDonations, SettingsUser, ChangePassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='main'),
    path('add-donation/', AddDonation.as_view(), name='donation'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('panel-admin/', AdminPanel.as_view(), name='p-admin'),
    path('panel-admin/edit-user/<int:user_id>', EditUser.as_view(), name='edit-user'),
    path('panel-admin/profil/', ProfilUser.as_view(), name='profil'),
    path('panel-admin/settings/', SettingsUser.as_view(), name='settings'),
    path('panel-admin/settings/change-password/', ChangePassword.as_view(), name='change-password'),
    path('panel-admin/profil/<int:donation_id>', ArchiveDonations.as_view(), name='archive'),
    path('panel-admin/delete-user/<int:user_id>', DeleteUser.as_view(), name='delete-user'),
    path('register/', Register.as_view(), name='register'),
    path('add-donation/confirmation/', FormConfirmationView.as_view(), name='confirmation'),


]
