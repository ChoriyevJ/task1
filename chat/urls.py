from django.urls import path

from chat import views


urlpatterns = [
    path('chat/list/', views.ChatListAPI.as_view())
]
