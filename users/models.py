from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
class User(AbstractUser):
    phone_number = models.CharField(max_length=14)


    @property
    def full_name(self):
        return self.first_name + self.last_name

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def __str__(self):
        return self.full_name


    def check_pass(self):
        if not self.password.startswith('pbkdf2'):
            self.set_password(self.password)


    def save(self, *args, **kwargs):
        self.check_pass()
        super(User, self).save(*args, **kwargs)
