# Generated by Django 3.2.5 on 2022-08-25 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0023_auto_20220824_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='25/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='25/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='25/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='25/08/2022', null=True),
        ),
    ]
