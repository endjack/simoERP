# Generated by Django 3.2.5 on 2021-10-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0017_auto_20211028_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='29/10/2021', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='29/10/2021', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='29/10/2021', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='29/10/2021', null=True),
        ),
    ]
