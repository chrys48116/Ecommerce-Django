from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf
from datetime import date


# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField(default=0)
    data_nasc = models.DateField(verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user}'
    
    def clean(self):
        atual = date.today().year
        error_messages = {}
    
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite apenas números.'

        if error_messages:
            raise ValidationError(error_messages)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'