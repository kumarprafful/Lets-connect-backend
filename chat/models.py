import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from core.models import TimeStampedMixin

User = get_user_model()


class RoomManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first_user=user) | Q(second_user=user)
        qlookup2 = Q(first_user=user) & Q(second_user=user)
        qs = self.get_queryset().filter(qlookup).distinct()
        return qs

    def get_or_new(self, first_user, second_user):
        first_user_id = first_user.id
        second_user_id = second_user.id

        qlookup1 = Q(first_user__id=first_user_id) & Q(second_user__id=second_user_id)
        qlookup2 = Q(first_user__id=second_user_id) & Q(second_user__id=first_user_id)
        qs = self.get_queryset().filter(qlookup1|qlookup2).distinct()

        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            a = qs.order_by('timestamp').first()
            return a, False
        else:
            obj = self.model(first_user=first_user, second_user=second_user)
            obj.save()
            return obj, True



class Room(TimeStampedMixin):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_first_name')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_second_name')

    objects = RoomManager()

    def __str__(self):
        return f'{self.first_user.email} - {self.second_user.email}'
    
    class Meta:
        unique_together = ['first_user', 'second_user']

    @property
    def get_initial_messages(self):
        return Message.objects.filter(room=self).order_by('-created_at')[:10]

    def get_last_message(self):
        return Message.objects.filter(room=self).latest('created_at')

class Message(TimeStampedMixin):
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.room.id} - {self.sender.email}'

