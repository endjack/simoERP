# Generated by Django 4.2.5 on 2023-10-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0008_funcionariov2_estado_civil'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariov2',
            name='cep_endereco',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]