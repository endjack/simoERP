# Generated by Django 3.2.5 on 2023-08-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0053_auto_20230804_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='07/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='07/08/2023', null=True),
        ),
    ]
