# Generated by Django 3.2.5 on 2021-08-27 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0014_alter_recibofornecedor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
    ]