# Generated by Django 3.2.5 on 2021-07-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, default='09/07/2021', null=True),
        ),
    ]
