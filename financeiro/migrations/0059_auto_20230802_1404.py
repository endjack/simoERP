# Generated by Django 3.2.5 on 2023-08-02 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0058_auto_20230728_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='02/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='02/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='02/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='02/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='02/08/2023', null=True),
        ),
    ]
