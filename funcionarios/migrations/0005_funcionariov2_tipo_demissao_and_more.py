# Generated by Django 4.2.4 on 2023-09-21 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0004_funcionariov2_dependentefuncionariov2'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariov2',
            name='tipo_demissao',
            field=models.CharField(choices=[('COM_JUSTA_CAUSA', 'Demissão POR justa causa'), ('SEM_JUSTA_CAUSA', 'Demissão SEM justa causa'), ('PEDIDO_POR_JUSTA_CAUSA', 'Pedido de demissão POR justa causa'), ('PEDIDO_SEM_JUSTA_CAUSA', 'Pedido de demissão SEM justa causa')], default='COM_JUSTA_CAUSA', max_length=50),
        ),
        migrations.CreateModel(
            name='ResponsávelObraFuncionariov2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsavel', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionariov2')),
            ],
        ),
        migrations.AddField(
            model_name='funcionariov2',
            name='responsavel_direto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='funcionarios.responsávelobrafuncionariov2'),
        ),
    ]