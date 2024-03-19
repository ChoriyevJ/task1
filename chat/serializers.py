from rest_framework import serializers

from chat.models import Chat, Message, Archive


class ChatSerializer(serializers.ModelSerializer):
    #
    sender = serializers.StringRelatedField(source='messages.username', read_only=True)
    receiver = serializers.StringRelatedField(source='messages.username', read_only=True)
    not_read = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chat
        fields = (
            'sender',
            'receiver',
            'not_read',
        )
