# Generated by Django 4.2.4 on 2023-09-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0072_alter_ordemservico_data_alter_servico_data_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='21/09/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='21/09/2023', null=True),
        ),
    ]
