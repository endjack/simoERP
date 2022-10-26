# Generated by Django 3.2.5 on 2022-09-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0029_auto_20220902_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='contapagamento',
            name='acrescimos',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='acrescimos'),
        ),
        migrations.AddField(
            model_name='contapagamento',
            name='nota_fiscal',
            field=models.CharField(blank=True, default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='05/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='05/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='05/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='05/09/2022', null=True),
        ),
    ]