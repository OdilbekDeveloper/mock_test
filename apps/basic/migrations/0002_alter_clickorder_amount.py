# Generated by Django 4.2.3 on 2023-12-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickorder',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
