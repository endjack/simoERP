# Generated by Django 3.2.4 on 2022-08-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0025_auto_20220826_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='29/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='29/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='29/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='29/08/2022', null=True),
        ),
    ]
