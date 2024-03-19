from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model


from utils.models import BaseModel


User = get_user_model()


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='receiver_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='sender_chats', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    audio = models.FileField(upload_to='audio', blank=True, null=True,
                             validators=[FileExtensionValidator(['mp3'])])
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} {self.text}"



class Contact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='contact_friends')
    friends = models.ManyToManyField(User, related_name='contacts')


class Chat(BaseModel):
    messages = models.ManyToManyField(Message, related_name='chats', blank=True)
    is_notificate = models.BooleanField(default=True)

    def __str__(self):
        return f'Chat(pk={self.pk})'



class Archive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='archives')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='archives')

    def __str__(self):
        return self.user.username



