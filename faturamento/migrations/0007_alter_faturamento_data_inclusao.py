# Generated by Django 3.2.5 on 2021-08-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0006_auto_20210813_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faturamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='20/08/2021', null=True),
        ),
    ]