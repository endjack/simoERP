# Generated by Django 4.2.5 on 2023-10-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0006_alter_funcionariov2_pix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariov2',
            name='nacionalidade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='funcionariov2',
            name='nome_mae',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='funcionariov2',
            name='nome_pai',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
