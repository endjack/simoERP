# Generated by Django 3.2.5 on 2023-08-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0057_auto_20230810_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='11/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='11/08/2023', null=True),
        ),
    ]
