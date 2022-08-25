# Generated by Django 3.2.5 on 2022-08-25 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0010_alter_itensselecionados_estoque'),
        ('requisicao', '0024_auto_20220825_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemrequisicao',
            name='item',
        ),
        migrations.AddField(
            model_name='itemrequisicao',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='estoque.estoque'),
        ),
    ]
