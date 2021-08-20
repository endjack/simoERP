# Generated by Django 3.2.5 on 2021-08-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='estoque/'),
        ),
        migrations.AddField(
            model_name='item',
            name='marca',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='unid_medida',
            field=models.CharField(choices=[('UNID', 'Unidade'), ('M', 'Metros'), ('M2', 'Metros2'), ('M3', 'Metros3'), ('CX', 'Caixa'), ('CJ', 'Conjunto'), ('PCT', 'Pacote'), ('PÇ', 'Peça'), ('TON', 'Tonelada'), ('L', 'Litros'), ('BD', 'Balde'), ('GL', 'Galão'), ('LT', 'Latão'), ('QTD', 'Quantidade')], default='UNID', max_length=50),
        ),
    ]
