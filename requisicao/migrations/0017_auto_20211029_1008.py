# Generated by Django 3.2.5 on 2021-10-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisicao', '0016_alter_requisicao_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequisicao',
            name='quantidade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requisicao',
            name='data',
            field=models.DateField(blank=True, default='29/10/2021', null=True),
        ),
    ]
