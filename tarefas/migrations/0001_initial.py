# Generated by Django 3.2.5 on 2021-08-25 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, null=True)),
                ('obs', models.TextField(blank=True, max_length=500, null=True)),
                ('data_inclusao', models.DateField(blank=True, null=True)),
                ('data_conclusao', models.DateField(blank=True, null=True)),
                ('feito', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('data_inclusao',),
            },
        ),
    ]
