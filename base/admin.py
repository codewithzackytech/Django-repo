from django.contrib import admin
from .models import Room, Message, Topic, User
from .form import doFollow

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'body', 'update', 'created']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'participants', 'update', 'created']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'bio']







admin.site.register(Room)

admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)

admin.site.register(Message, MessageAdmin)
