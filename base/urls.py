from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.Login, name='login'),
    path('logout/', views.logOutUser, name='logout'),
    path('register/', views.Register, name='register'),
    path('feedback/', views.feedBack, name='doFeedback'),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('getstart/', views.getStart, name='getstart'),

    path('', views.home, name="home"),
    path("room/<str:pk>/", views.room, name='room'),
    path('createRoom/', views.CreateRoom, name="create-room"),
    path('updateRoom/<str:pk>/', views.UpdateRoom, name="update-room"),
    path('deleteRoom/<str:pk>/', views.DeleteRoom, name="delete-room"),

    path('delete-message/<str:pk>/', views.DeleteMessage, name="delete-message"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('update-user/', views.updateUser, name="update-user"),

    #following
    path('follow/', views.doFollow, name="following")
]