from django.db import models


class Company(models.Model):
    name = models.CharField(verbose_name='Razão Social', max_length=200, unique=True)
    trading_name = models.CharField(verbose_name='Nome Fantasia', max_length=200, blank=True, null=True)
    registered_number = models.CharField(verbose_name='CNPJ', max_length=20, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    phone = models.CharField(verbose_name='Telefone', max_length=20, blank=True, null=True)

    employees = models.ManyToManyField('users.User', related_name='companies', verbose_name='Funcionários',
                                       through='Membership')

    class Meta:
        ordering = ['name', 'trading_name']

    def __str__(self):
        return self.name


class Membership(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} | {self.company}"
