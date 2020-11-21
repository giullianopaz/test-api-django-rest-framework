from django.db import models


class Company(models.Model):
    name = models.CharField(verbose_name='Razão Social', max_length=200, unique=True)
    trading_name = models.CharField(verbose_name='Nome Fantasia', max_length=200, blank=True, null=True)
    registered_number = models.CharField(verbose_name='CNPJ', max_length=20, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    phone = models.CharField(verbose_name='Telefone', max_length=20, blank=True, null=True)

    employees = models.ManyToManyField('users.User', verbose_name='Funcionários')

    class Meta:
        ordering = ['name', 'trading_name']

    def __str__(self):
        return self.name
