# Generated by Django 3.2.5 on 2022-08-31 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0025_alter_recibofornecedor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
