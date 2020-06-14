import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(user.password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_active', True)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superuser')
        return self._create_user(email, password, **kwargs)

    
class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{} {}".format(self.first_name or '', self.last_name or '')

    def save(self, *args, **kwargs):
        Contacts.objects.get_or_create(user=self)
        super(User, self).save(*args, **kwargs)


class Contacts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    contacts = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='contact_list')

