# Generated by Django 3.2.5 on 2022-08-19 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0007_alter_logmovimentacao_data_inclusao'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItensSelecionados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estoque', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='estoque.estoque')),
            ],
        ),
    ]
