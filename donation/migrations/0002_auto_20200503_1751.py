# Generated by Django 3.0.5 on 2020-05-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]