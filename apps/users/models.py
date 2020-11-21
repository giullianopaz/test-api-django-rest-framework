from django.contrib.auth.models import AbstractUser


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
