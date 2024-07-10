# Generated by Django 4.2.5 on 2024-06-28 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0007_alter_obra_tipo'),
        ('funcionarios', '0009_funcionariov2_cep_endereco'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalDeTrabalhoFuncionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcionario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionariov2')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obras.local')),
            ],
        ),
    ]
