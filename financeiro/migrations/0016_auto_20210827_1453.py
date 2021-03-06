# Generated by Django 3.2.5 on 2021-08-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0015_auto_20210826_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagConta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='data_inclusao',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='contapagamento',
            name='vencimento',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateField(blank=True, default='27/08/2021', null=True),
        ),
        migrations.AddField(
            model_name='contapagamento',
            name='tags',
            field=models.ManyToManyField(blank=True, to='financeiro.TagConta'),
        ),
    ]
