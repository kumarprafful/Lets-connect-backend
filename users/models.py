import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.conf import settings

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedMixin

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
        super(User, self).save(*args, **kwargs)
        Contacts.objects.get_or_create(user=self)


    def get_rooms(self):
        from chat.models import Room
        print(Room.objects.by_user(user=self))
        return list(Room.objects.by_user(user=self).values_list('id', flat=True))

    def get_room_id(self, other_user):
        from chat.models import Room
        room, _ =  Room.objects.get_or_new(first_user=self, second_user=other_user)
        return room.id

    def last_message(self, other_user):
        try:
            from chat.models import Room
            room, _ =  Room.objects.get_or_new(first_user=self, second_user=other_user)
            return room.get_last_message()
        except:
            return None
        
class Contacts(TimeStampedMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    contacts = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='contact_list')


class Invites(TimeStampedMixin):
    invited_by = models.ForeignKey(User, related_name='invited_by', on_delete=models.DO_NOTHING)
    invited_user = models.ForeignKey(User, related_name='invited_user', blank=True, null=True, on_delete=models.CASCADE)
    invited_email = models.EmailField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('invited_by', 'invited_user'),
            ('invited_by', 'invited_email'),
        )