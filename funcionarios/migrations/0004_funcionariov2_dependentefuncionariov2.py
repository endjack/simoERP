# Generated by Django 4.2.4 on 2023-09-20 14:41

from django.db import migrations, models
import django.db.models.deletion
import funcionarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedores', '0002_auto_20210708_1133'),
        ('obras', '0007_alter_obra_tipo'),
        ('funcionarios', '0003_auto_20210721_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncionarioV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situacao', models.CharField(choices=[('ADMITIDO', 'Admitido'), ('DEMITIDO', 'Demitido'), ('AFASTADO INSS - POR DOENÇA', 'Afastado por Doença'), ('AFASTADO INSS - POR ACIDENTE', 'Afastado por Acidente')], default='ADMITIDO', max_length=50)),
                ('matricula', models.CharField(blank=True, max_length=20, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='funcionarios/', validators=[funcionarios.models.FuncionarioV2.validate_image])),
                ('nome', models.CharField(max_length=200)),
                ('cpf', models.CharField(blank=True, max_length=20, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, null=True)),
                ('ctps', models.CharField(blank=True, max_length=30, null=True)),
                ('cnh', models.CharField(blank=True, max_length=30, null=True)),
                ('categoria_cnh', models.CharField(blank=True, max_length=20, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('endereco', models.CharField(blank=True, max_length=200, null=True)),
                ('telefone1', models.CharField(blank=True, max_length=20, null=True)),
                ('telefone2', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo_contrato', models.CharField(choices=[('DETERMINADO', 'Prazo Determinado'), ('INDETERMINADO', 'Prazo Indeterminado')], default='DETERMINADO', max_length=20)),
                ('data_admissao', models.DateField(blank=True, null=True)),
                ('data_inicio_prorrogacao', models.DateField(blank=True, null=True)),
                ('data_fim_prorrogacao', models.DateField(blank=True, null=True)),
                ('data_inicio_afastamento', models.DateField(blank=True, null=True)),
                ('data_fim_afastamento', models.DateField(blank=True, null=True)),
                ('data_ultimo_exame', models.DateField(blank=True, null=True)),
                ('data_demissao', models.DateField(blank=True, null=True)),
                ('salario', models.FloatField(default=0, max_length=20)),
                ('adicional', models.FloatField(default=0, max_length=20)),
                ('obs', models.TextField(blank=True, max_length=200, null=True)),
                ('agencia', models.CharField(blank=True, max_length=10, null=True)),
                ('tipo_conta', models.CharField(choices=[('CONTA-CORRENTE', 'Conta-Corrente'), ('POUPANÇA', 'Poupança'), ('CONTA-PAGAMENTO', 'Conta-pagamento')], default='CONTA-CORRENTE', max_length=50)),
                ('op', models.CharField(blank=True, max_length=10, null=True)),
                ('conta', models.CharField(blank=True, max_length=10, null=True)),
                ('pix', models.CharField(blank=True, max_length=10, null=True)),
                ('tipo_pix', models.CharField(choices=[('CPF', 'CPF'), ('CNPJ', 'CNPJ'), ('TELEFONE', 'Telefone'), ('E-MAIL', 'E-mail'), ('ALEATÓRIO', 'Aleatório')], default='CPF', max_length=50)),
                ('esocial', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo_responsavel', models.BooleanField(default=False)),
                ('analfabeto', models.BooleanField(default=False)),
                ('data_cadastro', models.DateField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
                ('banco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fornecedores.banco')),
                ('cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='funcionarios.cargo')),
                ('lotacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='obras.obra')),
            ],
        ),
        migrations.CreateModel(
            name='DependenteFuncionariov2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cpf', models.CharField(blank=True, max_length=20, null=True)),
                ('funcionario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionariov2')),
            ],
        ),
    ]
