# Generated by Django 3.1.1 on 2020-11-11 19:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='contact_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='^[0-9]{10}$')]),
        ),
    ]
