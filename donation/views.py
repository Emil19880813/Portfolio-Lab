from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from donation.forms import RegisterForm, LoginForm
from donation.models import Donation, Institution, Category

'''
class LandingPage(TemplateView):
    template_name = "index.html"
'''

class LandingPage(View):
    def get(self, request):
        donations = list(Donation.objects.aggregate(Sum('quantity')).values())[0]
        institutions = len([donation.institution.name for donation in Donation.objects.all().distinct('institution')])
        foundations = Institution.objects.filter(type="Fundacja")
        organisations = Institution.objects.filter(type="Organizacja pozarządowa")
        locals = Institution.objects.filter(type="Zbiórka lokalna")

        def num_of_pages(obj):
            p = Paginator(obj, 3) # show 5 objects per page.
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
        cat = Category.objects.all()
        return render(request, 'form.html', context={'categories': cat})

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

class FormConfirmationView(TemplateView):
    template_name = "form-confirmation.html"