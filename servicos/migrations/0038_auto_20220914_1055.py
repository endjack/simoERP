# Generated by Django 3.2.5 on 2022-09-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0037_auto_20220913_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='14/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='14/09/2022', null=True),
        ),
    ]