# Generated by Django 3.2.5 on 2023-08-24 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0063_auto_20230823_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='24/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='24/08/2023', null=True),
        ),
    ]