# Generated by Django 4.2.5 on 2024-07-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0065_auto_20230830_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
    ]
