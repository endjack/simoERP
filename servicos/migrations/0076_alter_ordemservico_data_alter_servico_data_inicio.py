# Generated by Django 4.2.5 on 2024-06-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0075_alter_ordemservico_data_alter_servico_data_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='28/06/2024', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='28/06/2024', null=True),
        ),
    ]