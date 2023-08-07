# Generated by Django 3.2.5 on 2023-08-07 10:36

from django.db import migrations, models
import obras.models


class Migration(migrations.Migration):

    dependencies = [
        ('obras', '0004_obra_concluido'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to=obras.models.def_pasta_upload_imagem),
        ),
        migrations.AddField(
            model_name='obra',
            name='invisivel',
            field=models.BooleanField(default=False),
        ),
    ]
