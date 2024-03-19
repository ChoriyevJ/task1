from django.urls import path

from chat import views


urlpatterns = [
    path('chat/', views.ChatListAPI.as_view())
]
