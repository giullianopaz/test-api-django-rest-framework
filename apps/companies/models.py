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

    @classmethod
    def get_existing_by_pk(cls, companies):
        """
        Recebe uma lista de ids e retorna os objetos que existem, a partir dos ids.
        Isso evita ficar testando a existência de objetos constantemente.
        """
        if companies is None or len(companies) == 0:
            return []
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        return [company for company in cls.objects.filter(pk__in=companies)]

    def add_employees(self, employees):
        if employees is None:
            return
        employees = [employees] if not isinstance(employees, (list, tuple)) else employees
        for employee in employees:
            if not Membership.objects.filter(company=self, user=employee).exists():
                Membership.objects.create(
                    company=self,
                    user=employee
                )

    def get_employees(self):
        return self.employees.all()

    def update_employees(self, employees):
        if employees is None:
            return
        self.employees.clear()
        employees = [employees] if not isinstance(employees, (list, tuple)) else employees
        for employee in employees:
            if not Membership.objects.filter(company=self, user=employee).exists():
                Membership.objects.create(
                    company=self,
                    user=employee
                )

    def delete_employees(self, employees):
        if employees is None:
            return
        employees = [employees] if not isinstance(employees, (list, tuple)) else employees
        for employee in employees:
            self.employees.remove(employee)

    def clean_employees(self):
        self.employees.clear()


class Membership(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} | {self.company}"
