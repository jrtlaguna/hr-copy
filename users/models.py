from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    middle_name = models.CharField("Middle Name", max_length=150, **OPTIONAL)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_full_name()
