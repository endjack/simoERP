# Generated by Django 3.2.5 on 2021-08-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0014_auto_20210825_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='26/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='26/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='26/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='26/08/2021', null=True),
        ),
    ]
