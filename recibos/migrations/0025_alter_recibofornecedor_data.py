# Generated by Django 3.2.4 on 2022-08-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0024_alter_recibofornecedor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, default='29/08/2022', null=True),
        ),
    ]
