# Generated by Django 3.2.5 on 2021-07-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='09/07/2021', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='09/07/2021', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='09/07/2021', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='09/07/2021', null=True),
        ),
    ]
