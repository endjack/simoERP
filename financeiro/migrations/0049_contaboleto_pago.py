# Generated by Django 3.2.5 on 2022-09-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0048_auto_20220920_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='contaboleto',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]
