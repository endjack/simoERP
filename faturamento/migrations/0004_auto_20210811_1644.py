# Generated by Django 3.2.5 on 2021-08-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0003_alter_faturamento_data_pagamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faturamento',
            name='documento',
        ),
        migrations.AddField(
            model_name='faturamento',
            name='situacao',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
