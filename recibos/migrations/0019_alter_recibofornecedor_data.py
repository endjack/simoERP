# Generated by Django 3.2.5 on 2022-08-17 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibos', '0018_alter_recibofornecedor_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibofornecedor',
            name='data',
            field=models.DateField(blank=True, default='17/08/2022', null=True),
        ),
    ]
