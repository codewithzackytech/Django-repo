from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, UserFeedback
from .form import RoomForm, UserForm, MyUserCreationForm, TopicForm, doFollow, UserForm2, UserFeedbackForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer, Serializer
from base.models import Room
import json


def getStart(request):
    return render(request, 'index.html')


def home(request):
    x = 1
    y = 2
    room_count = ''
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        room_count = user.room_set.count
        
    public_User = User.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    data = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # data = Room.objects.all()
    #print(f"q is equal to: {q}")
    topic = Topic.objects.all()





    room_message = Message.objects.filter(Q(room__name__icontains=q))  # each topic should use only there activity
    
    fUser = request.POST.get("fUser")
    
  
    return render(request, 'base/index.html', {
        'data': data,
        'topic': topic,
        'room_messages': room_message,
        'room_count': room_count,
        'public_User':public_User
    })
    
         


def room(request, pk):


    room = Room.objects.get(id=pk)
    roommessage = room.message_set.all()  # .order_by('-created')

    participants = room.participants.all()
    context = {'room': room, 'roommessage': roommessage, 'participants': participants}
    if request.method == 'POST':
        if request.user.is_authenticated:
            message = Message.objects.create(
                user=request.user,
                room=room,

                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        else:
            return redirect('login')
    return render(request, 'base/room.html', context)

@login_required(login_url='login')

def userProfile(request, pk):


    user = User.objects.get(id=pk)
    data = user.room_set.all()


    room_count = user.room_set.count


    postLoop = [{'id': 1, 'name': 'af'}]
    room_messages = user.message_set.all()

    topic = Topic.objects.all()

    context = {
        'postLoop': postLoop,
        'user': user,
        'data': data,
        'room_count':room_count,
        'room_messages': room_messages,
        'topic': topic
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def CreateRoom(request):
 
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        topic_name = request.POST.get('topic_name')
        description = request.POST.get('description')
      
        topic, created = Topic.objects.get_or_create(name=topic_name)

    
        if form.is_valid():
            save = form.save()
            save.host = request.user
            save.topic = topic
            save.name =description[0:50]
            save.save()
            return redirect('home')

    content = {'form': form,


               }

    # topics = tpc.room_set.all()
    return render(request, 'base/room_form.html', content)


@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form

    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def DeleteRoom(request, pk):
    form = Room.objects.get(id=pk)
    if request.user != form.host:
        return HttpResponse('your are not allowed to be here!')

    if request.method == 'POST':
        form.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'form': form})


def Login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                userCheck = User.objects.get(username=username)
            except:
                messages.info(request, "Access denied")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logOutUser(request):
    logout(request)
    return redirect('home')


def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        page = 'register'
        form = MyUserCreationForm()
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            backUpPasssword = request.POST.get('password1')
            name = request.POST.get('first_name')
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.backUpPasssword = backUpPasssword
                user.name = name
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "wrong registration")

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login')
def DeleteMessage(request, pk):
    form = Message.objects.get(id=pk)
    if request.user != form.user:
        return HttpResponse('your are not allowed to be here!')

    if request.method == 'POST':
        form.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    public_User = User.objects.all()

    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics,
        'public_User':public_User
    }
    return render(request, 'base/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()  # each topic should use only there activity
    topic = Topic.objects.all()
    context = {'room_messages': room_messages, 'topic':topic}
    return render(request, 'base/activity.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {
        'form': form

    }

    return render(request, 'base/update_user.html', context)




@login_required(login_url='login')
def doFollow(request):

    user = request.user

    form = UserForm2(instance=user)

    user2 = request.POST.get('userE')
    context = {
        'form': form,
        'user2':user2

    }

    if request.method == 'POST':



        #print("\n\n\n\n hhhhh\n\n")
        print(request.POST.get('followersPeople'))

        form = UserForm2(request.POST, request.FILES, instance=user)
        if form.is_valid():

            form.save()
            return redirect('home')
    return render(request, 'base/update_user_follow.html', context)


@login_required(login_url='login')
def feedBack(request):
    form = UserFeedbackForm()

    # saving feedback.


    if request.method == 'POST':

        
        email = request.POST.get('email')
        body = request.POST.get('body')
        
        UserFeedback.objects.create(
            email=request.user,
            body=body
        )









    content = {}
    return render(request, 'base/feedback.html', content)