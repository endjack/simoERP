# Generated by Django 4.2.5 on 2023-10-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0007_funcionariov2_nacionalidade_funcionariov2_nome_mae_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariov2',
            name='estado_civil',
            field=models.CharField(choices=[('SOLTEIRO', 'SOLTEIRO'), ('CASADO', 'CASADO'), ('SEPARADO', 'SEPARADO'), ('DIVORCIADO', 'DIVORCIADO'), ('VIÚVO', 'VIÚVO')], default='SOLTEIRO', max_length=50),
        ),
    ]