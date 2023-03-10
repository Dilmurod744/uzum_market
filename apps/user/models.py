from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField


class User(AbstractUser):
    class Type(TextChoices):
        MERCHANT = 'merchant', 'Sotuvchi'
        CLIENT = 'client', 'Haridor'

    type = CharField(max_length=25, choices=Type.choices, default=Type.CLIENT)
