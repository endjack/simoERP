# Generated by Django 3.2.5 on 2023-08-03 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engenharia', '0011_auto_20230803_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diariodeobraos',
            name='ocorrencias',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]