# Generated by Django 3.2.5 on 2021-10-28 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_alter_estoque_quantidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='marca',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
