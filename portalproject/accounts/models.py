from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ''' Extended Uer Model '''

    class Meta:
        verbose_name_plural = 'CustomUser'

