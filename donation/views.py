from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.utils import timezone

import datetime

from donation.forms import RegisterForm, LoginForm, UserForm, SettingsUserForm
from donation.models import Donation, Institution, Category

'''
class LandingPage(TemplateView):
    template_name = "index.html"
'''
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')

class LandingPage(LoginRequiredMixin, View):
    def get(self, request):
        donations = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = len([donation.institution.name for donation in Donation.objects.all().distinct('institution')])
        foundations = Institution.objects.filter(type="Fundacja")
        organisations = Institution.objects.filter(type="Organizacja pozarządowa")
        locals = Institution.objects.filter(type="Zbiórka lokalna")

        def num_of_pages(obj):
            p = Paginator(obj, 3) # show 3 objects per page.
            page_number = request.GET.get('page')

            if page_number is None:
                return p.get_page(1)

            return p.get_page(page_number)

        return render(request, "index.html", {"donations": donations, "institutions": institutions,
                                              "foundations": num_of_pages(foundations),
                                              "organisations": num_of_pages(organisations),
                                              "locals": num_of_pages(locals)})

class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', context={'categories': categories, 'institutions': institutions})


class Login(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html", context={"form": login_form})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return redirect('register')
        return redirect('register')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('register')


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', context={'form': form})
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()
            return redirect('login')
        return render(request, 'register.html', context={'form': form})

class AdminPanel(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'panel-admin.html', context={'users': users})


class AddUser(View):
    def get(self, request):
        user_form = UserForm()
        return render(request, "add_user.html", context={"form": user_form})
    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
        return redirect('p-admin')


class EditUser(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user_form = UserForm(instance=user)
        return render(request, "edit_user.html", context={"form": user_form})
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('p-admin')

class DeleteUser(View):
    def get(self, request, user_id):
        User.objects.get(pk=user_id).delete()
        return redirect('p-admin')


class ProfilUser(View):
    def get(self, request):
        user = request.user
        donation_list = user.donations.all().order_by('is_taken', 'pick_up_date', 'pick_up_time', 'date_of_entry')
        return render(request, "profil_user.html", context={'user': user, 'donations': donation_list})


class ArchiveDonations(View):
    def get(self, request, donation_id):
        donation = Donation.objects.get(pk=donation_id)
        if donation.is_taken:
            donation.is_taken = False
            donation.pick_up_date = None
            donation.pick_up_time = None
            donation.save()
        else:
            donation.is_taken = True
            donation.pick_up_date = datetime.datetime.now()
            donation.pick_up_time = timezone.now()
            donation.save()
        return redirect('profil')

class SettingsUser(View):
    def get(self, request):
        user = request.user
        user_form = SettingsUserForm(instance=user)
        return render(request, "settings.html", context={"form": user_form})

    def post(self, request):
        user = request.user
        user_form = SettingsUserForm(request.POST, instance=user)
        if user_form.is_valid():
            if user.check_password(user_form.cleaned_data.get('password')):
                user_form.save()
                return redirect('profil')
            return redirect('settings')

class FormConfirmationView(TemplateView):
    template_name = "form-confirmation.html"