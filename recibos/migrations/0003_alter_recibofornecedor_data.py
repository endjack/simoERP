# Generated by Django 3.2.5 on 2021-07-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0002_alter_recibofornecedor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, default='14/07/2021', null=True),
        ),
    ]
