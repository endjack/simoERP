# Generated by Django 3.2.5 on 2022-08-24 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0016_alter_faturamento_data_inclusao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faturamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='24/08/2022', null=True),
        ),
    ]
