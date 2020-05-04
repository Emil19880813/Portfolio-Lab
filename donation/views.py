from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from donation.models import Donation, Institution

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
            p = Paginator(obj, 3) # show 3 objects per page.
            page_number = request.GET.get('page')

            if page_number is None:
                return p.get_page(1)

            return p.get_page(page_number)

        return render(request, "index.html", {"donations": donations, "institutions": institutions,
                                              "foundations": num_of_pages(foundations),
                                              "organisations": num_of_pages(organisations),
                                              "locals": num_of_pages(locals)})

class AddDonation(TemplateView):
    template_name = "form.html"

class Login(TemplateView):
    template_name = "login.html"

class Register(TemplateView):
    template_name = "register.html"

class FormConfirmationView(TemplateView):
    template_name = "form-confirmation.html"