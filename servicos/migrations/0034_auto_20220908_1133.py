# Generated by Django 3.2.5 on 2022-09-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0033_auto_20220906_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='08/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='08/09/2022', null=True),
        ),
    ]
