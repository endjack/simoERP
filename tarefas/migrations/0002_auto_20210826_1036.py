# Generated by Django 3.2.5 on 2021-08-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='data_conclusao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='data_inclusao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
