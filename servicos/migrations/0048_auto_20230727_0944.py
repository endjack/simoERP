# Generated by Django 3.2.5 on 2023-07-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0047_auto_20230707_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='27/07/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='27/07/2023', null=True),
        ),
    ]
