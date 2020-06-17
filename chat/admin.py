from django.contrib import admin

from chat.models import Room, Message

class Message(admin.TabularInline):
    model = Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [Message]
    class Meta:
        model = Room
