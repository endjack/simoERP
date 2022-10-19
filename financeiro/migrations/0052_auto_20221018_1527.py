# Generated by Django 3.2.5 on 2022-10-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0051_auto_20220922_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamentoboleto',
            name='acrescimo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='18/10/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='18/10/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='18/10/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='18/10/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='18/10/2022', null=True),
        ),
    ]
