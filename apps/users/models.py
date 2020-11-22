from django.contrib.auth.models import AbstractUser

from apps.companies.models import Company, Membership


class User(AbstractUser):
    """
    Model customizada de usuários. Com essa model, é possível adicionar campos e comportamentos à model de usuários.
    Isso não seria possível fazer com a model padrão do Django.
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'
        ordering = ['pk']

    def __str__(self):
        return self.get_full_name()

    def add_companies(self, companies):
        if companies is None:
            return
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company_pk in companies:
            if Company.objects.filter(pk=company_pk).exists():
                company_instance = Company.objects.get(pk=company_pk)
                if not Membership.objects.filter(company=company_instance, user=self).exists():
                    Membership.objects.create(
                        company=company_instance,
                        user=self
                    )

    def get_companies(self):
        return self.companies.all()

    def update_companies(self, companies):
        if companies is None:
            return
        self.companies.clear()
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company_pk in companies:
            if Company.objects.filter(pk=company_pk).exists():
                company_instance = Company.objects.get(pk=company_pk)
                if not Membership.objects.filter(company=company_instance, user=self).exists():
                    Membership.objects.create(
                        company=company_instance,
                        user=self
                    )

    def delete_companies(self, companies):
        if companies is None:
            return
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company_pk in companies:
            if Company.objects.filter(pk=company_pk).exists():
                company_instance = Company.objects.get(pk=company_pk)
                company_instance.employees.remove(self)

    def clean_companies(self):
        self.companies.clear()
