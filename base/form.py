from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Topic, UserFeedback
#from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants', 'GTopic', 'host', 'topic', 'name']


class UserFeedbackForm(ModelForm):
    class Meta:
        model = UserFeedback
        fields = '__all__'
        #exclude = ['email']

class doFollow(ModelForm):
    class Meta:
        model = User
        fields = ['followersPeople']

        
class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avator', 'name', 'username', 'email', 'bio']



class UserForm2(ModelForm):
    class Meta:
        model = User
        fields = ['followersPeople']

