# Generated by Django 3.2.5 on 2021-08-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisicao', '0008_alter_requisicao_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicao',
            name='data',
            field=models.DateField(blank=True, default='11/08/2021', null=True),
        ),
    ]
