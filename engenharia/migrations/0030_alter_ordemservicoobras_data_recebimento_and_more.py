# Generated by Django 4.2.5 on 2024-09-04 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('obras', '0007_alter_obra_tipo'),
        ('engenharia', '0029_alter_diariodeobraos_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservicoobras',
            name='data_recebimento',
            field=models.DateField(blank=True, default='04/09/2024', null=True),
        ),
        migrations.CreateModel(
            name='DiarioDeObraContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True)),
                ('atividades', models.TextField(blank=True, max_length=500, null=True)),
                ('ordem_servico', models.CharField(blank=True, max_length=200, null=True)),
                ('tempo_manha', models.CharField(blank=True, max_length=200, null=True)),
                ('tempo_tarde', models.CharField(blank=True, max_length=200, null=True)),
                ('equipamentos', models.TextField(blank=True, max_length=500, null=True)),
                ('mao_de_obra', models.TextField(blank=True, max_length=500, null=True)),
                ('ocorrencias', models.TextField(blank=True, max_length=1000, null=True)),
                ('obra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='obras.obra')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]