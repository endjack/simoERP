# Generated by Django 3.2.5 on 2021-08-26 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0003_auto_20210826_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='cor',
            field=models.CharField(blank=True, choices=[('#ffffff', 'Branco'), ('#ffebcd', 'Creme'), ('#87cefa', 'Azul Claro'), ('#c8a2c8', 'Lilás'), ('#e4f1cb', 'Verde Claro'), ('#dedede', 'Cinza')], default='#ffffff', max_length=30),
        ),
    ]