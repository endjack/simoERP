# Generated by Django 3.2.5 on 2023-08-10 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0065_auto_20230809_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='10/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='10/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='10/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='10/08/2023', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='10/08/2023', null=True),
        ),
    ]