# Generated by Django 3.2.5 on 2021-08-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0002_alter_faturamento_num_medicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faturamento',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
