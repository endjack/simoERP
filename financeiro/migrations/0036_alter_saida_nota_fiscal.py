# Generated by Django 3.2.5 on 2022-09-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0035_auto_20220908_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saida',
            name='nota_fiscal',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
