# Generated by Django 3.2.5 on 2021-08-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0009_auto_20210805_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='11/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='11/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='11/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='11/08/2021', null=True),
        ),
    ]
