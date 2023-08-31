# Generated by Django 4.2.4 on 2023-08-31 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0012_alter_logmovimentacao_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='estocado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='unid_medida',
            field=models.CharField(choices=[('UNID', 'Unidade'), ('KG', 'Quilos'), ('M', 'Metros'), ('M2', 'Metros2'), ('M3', 'Metros3'), ('CX', 'Caixa'), ('CJ', 'Conjunto'), ('PCT', 'Pacote'), ('PÇ', 'Peça'), ('TON', 'Tonelada'), ('L', 'Litros'), ('BD', 'Balde'), ('GL', 'Galão'), ('LT', 'Latão'), ('QTD', 'Quantidade')], default='UNID', max_length=50),
        ),
    ]