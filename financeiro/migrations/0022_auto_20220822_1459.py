# Generated by Django 3.2.5 on 2022-08-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0021_auto_20220819_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='22/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='22/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='22/08/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='22/08/2022', null=True),
        ),
    ]
