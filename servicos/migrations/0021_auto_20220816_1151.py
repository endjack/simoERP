# Generated by Django 3.2.5 on 2022-08-16 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0020_auto_20211029_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='16/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='16/08/2022', null=True),
        ),
    ]
