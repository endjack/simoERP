# Generated by Django 4.2.5 on 2024-07-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0074_auto_20230830_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacompleta',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='10/07/2024', null=True),
        ),
    ]