# Generated by Django 3.2.5 on 2022-09-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0040_auto_20220909_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itensnota',
            name='qtd',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=20, null=True),
        ),
    ]
