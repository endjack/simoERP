# Generated by Django 4.2.5 on 2024-05-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('engenharia', '0037_alter_diariodeobraos_data_and_more'), ('engenharia', '0038_alter_diariodeobraos_data_and_more')]

    dependencies = [
        ('engenharia', '0036_alter_diariodeobraos_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diariodeobraos',
            name='data',
            field=models.DateField(default='02/10/2023'),
        ),
        migrations.AlterField(
            model_name='ordemservicoobras',
            name='data_recebimento',
            field=models.DateField(blank=True, default='02/10/2023', null=True),
        ),
       
    ]
