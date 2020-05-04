from django.contrib import admin

# Register your models here.
from donation.models import Donation, Institution, Category

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
