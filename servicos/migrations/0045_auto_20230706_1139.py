# Generated by Django 3.2.5 on 2023-07-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0044_auto_20230607_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='numero_os',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(blank=True, default='06/07/2023', null=True),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_inicio',
            field=models.DateField(blank=True, default='06/07/2023', null=True),
        ),
    ]