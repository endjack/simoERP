# Generated by Django 3.2.5 on 2021-08-27 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0016_auto_20210826_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
    ]