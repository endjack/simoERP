# Generated by Django 3.2.5 on 2023-08-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engenharia', '0013_auto_20230804_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diariodeobraos',
            name='data',
            field=models.DateField(default='07/08/2023'),
        ),
        migrations.AlterField(
            model_name='ordemservicoobras',
            name='data_recebimento',
            field=models.DateField(blank=True, default='07/08/2023', null=True),
        ),
    ]
