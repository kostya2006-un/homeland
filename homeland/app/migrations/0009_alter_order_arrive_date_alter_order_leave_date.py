# Generated by Django 4.2.1 on 2023-11-28 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_order_arrive_date_alter_order_leave_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='arrive_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='leave_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
