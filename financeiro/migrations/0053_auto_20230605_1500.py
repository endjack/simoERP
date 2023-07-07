# Generated by Django 3.2.5 on 2023-06-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0052_auto_20221018_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='05/06/2023', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='05/06/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='05/06/2023', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='05/06/2023', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='05/06/2023', null=True),
        ),
    ]