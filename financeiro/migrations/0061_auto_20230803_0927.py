# Generated by Django 3.2.5 on 2023-08-03 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0060_merge_0059_auto_20230802_0003_0059_auto_20230802_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
    ]
