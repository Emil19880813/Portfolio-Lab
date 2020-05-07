from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(null=False)
    categories = models.ManyToManyField('Category', related_name='donations')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='donations')
    address = models.CharField(max_length=255, null=False)
    phone_number = models.IntegerField(null=False, blank=True)
    city = models.CharField(max_length=128, null=False)
    zip_code = models.CharField(max_length=6, blank=True)
    pick_up_date = models.DateField(null=False)
    pick_up_time = models.TimeField(null=False)
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='donations')

    def __str__(self):
        return f"""( worki - {self.quantity} , kategorie - {", ".join(category.name for category in self.categories.all())}, 
                    instytucja - {self.institution.name}, użytkownik - {self.user.username})"""


class Institution(models.Model):
    INSTITUTIONS = (
        ('Fundacja', 'Fundacja'),
        ('Organizacja pozarządowa', 'Organizacja pozarządowa'),
        ('Zbiórka lokalna', 'Zbiórka lokalna'),
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=25, choices=INSTITUTIONS, default='Fundacja')
    categories = models.ManyToManyField('Category', related_name='institutions')

    def __str__(self):
        return self.name