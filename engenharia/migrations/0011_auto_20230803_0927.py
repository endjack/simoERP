# Generated by Django 3.2.5 on 2023-08-03 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('engenharia', '0010_auto_20230802_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiarioDeObraOs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default='03/08/2023')),
                ('atividades', models.TextField(blank=True, max_length=500, null=True)),
                ('tempo_manha', models.CharField(blank=True, max_length=200, null=True)),
                ('tempo_tarde', models.CharField(blank=True, max_length=200, null=True)),
                ('equipamentos', models.TextField(blank=True, max_length=500, null=True)),
                ('mao_de_obra', models.TextField(blank=True, max_length=500, null=True)),
                ('ocorrencias', models.TextField(blank=True, max_length=500, null=True)),
                ('fotos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='engenharia.categoriaimagem')),
            ],
        ),
        migrations.AlterField(
            model_name='ordemservicoobras',
            name='data_recebimento',
            field=models.DateField(blank=True, default='03/08/2023', null=True),
        ),
        migrations.DeleteModel(
            name='RegistroOs',
        ),
        migrations.AddField(
            model_name='diariodeobraos',
            name='ordem_servico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='engenharia.ordemservicoobras'),
        ),
        migrations.AddField(
            model_name='diariodeobraos',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
