# Generated by Django 3.2.5 on 2021-07-16 11:54

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='local',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('local'), nulls_last=True)]},
        ),
        migrations.AlterModelOptions(
            name='obra',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('nome'), nulls_last=True)]},
        ),
    ]
