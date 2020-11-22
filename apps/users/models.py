from django.contrib.auth.models import AbstractUser

from apps.companies.models import Membership


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

    @classmethod
    def get_existing_by_pk(cls, users):
        """
        Recebe uma lista de ids e retorna os objetos que existem, a partir dos ids.
        Isso evita ficar testando a existência de objetos constantemente.
        """
        if users is None or len(users) == 0:
            return []
        users = [users] if not isinstance(users, (list, tuple)) else users
        return [user for user in cls.objects.filter(pk__in=users)]

    def add_companies(self, companies):
        if companies is None:
            return
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company in companies:
            if not Membership.objects.filter(company=company, user=self).exists():
                Membership.objects.create(
                    company=company,
                    user=self
                )

    def get_companies(self):
        return self.companies.all()

    def update_companies(self, companies):
        if companies is None:
            return
        self.companies.clear()
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company in companies:
            if not Membership.objects.filter(company=company, user=self).exists():
                Membership.objects.create(
                    company=company,
                    user=self
                )

    def delete_companies(self, companies):
        if companies is None:
            return
        companies = [companies] if not isinstance(companies, (list, tuple)) else companies
        for company in companies:
            company.employees.remove(self)

    def clean_companies(self):
        self.companies.clear()
