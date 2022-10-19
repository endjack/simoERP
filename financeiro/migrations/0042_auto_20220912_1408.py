# Generated by Django 3.2.5 on 2022-09-12 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financeiro', '0041_alter_itensnota_qtd'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagamentoVista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_pago', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='valor')),
                ('acrescimo', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='valor')),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('obs', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='notacompleta',
            name='data_pagamento',
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='12/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='12/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='12/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='pagamentotemp',
            name='data',
            field=models.DateField(blank=True, default='12/09/2022', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='12/09/2022', null=True),
        ),
        migrations.DeleteModel(
            name='ItensSaidaTemp',
        ),
        migrations.AddField(
            model_name='pagamentovista',
            name='conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='financeiro.notacompleta'),
        ),
        migrations.AddField(
            model_name='pagamentovista',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
