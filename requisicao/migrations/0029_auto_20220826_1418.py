# Generated by Django 3.2.5 on 2022-08-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisicao', '0028_requisicaotemp_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicao',
            name='data',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='requisicaotemp',
            name='data',
            field=models.DateTimeField(null=True),
        ),
    ]
