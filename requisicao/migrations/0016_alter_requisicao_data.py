# Generated by Django 3.2.5 on 2021-10-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisicao', '0015_alter_requisicao_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicao',
            name='data',
            field=models.DateField(blank=True, default='28/10/2021', null=True),
        ),
    ]
