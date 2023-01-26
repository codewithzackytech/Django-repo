from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, default="Focusing on future")
    backUpPasssword = models.CharField(max_length=2083, null=True)
    followersPeople = models.IntegerField(blank=True, null=True)

    avator = models.ImageField(default="userLogo.png", null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['email', '-bio']

# user feedback

class UserFeedback(models.Model):
    body = models.TextField(max_length=2080)
    email = models.CharField(max_length=50)   


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  #topic specification
    name = models.CharField(max_length=200)
    Image_If_Needed = models.ImageField(default="defaultPost.jpg", null=True)
    description = models.TextField(null=True, blank=True, max_length=2080)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    
    # GTopic should be image_status = models.BooleanField()
    GTopic = models.CharField(max_length=50, null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)




    class Meta:
        ordering = ['-created', '-update']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(max_length=2080)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created']


    def __str__(self):
        return self.body[0:50]