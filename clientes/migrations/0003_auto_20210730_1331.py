# Generated by Django 3.2.5 on 2021-07-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_cliente_obra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('doc', models.CharField(blank=True, max_length=50, null=True)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cargo',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='obra',
        ),
    ]
