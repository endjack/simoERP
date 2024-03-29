# Generated by Django 3.2.5 on 2023-08-23 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque_v2', '0002_auto_20230823_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='ferramenta',
            name='cor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ferramenta',
            name='estado',
            field=models.CharField(choices=[(0, 'NOVA'), (1, 'USADA'), (3, 'COM DEFEITO')], default=1, max_length=50),
        ),
        migrations.AddField(
            model_name='ferramenta',
            name='numeracao',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ferramenta',
            name='tamanho',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
