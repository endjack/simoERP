# Generated by Django 3.2.5 on 2023-08-24 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engenharia', '0025_auto_20230823_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diariodeobraos',
            name='data',
            field=models.DateField(default='24/08/2023'),
        ),
        migrations.AlterField(
            model_name='ordemservicoobras',
            name='data_recebimento',
            field=models.DateField(blank=True, default='24/08/2023', null=True),
        ),
    ]