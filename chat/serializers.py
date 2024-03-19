from rest_framework import serializers

from chat.models import Chat, Message, Archive


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.StringRelatedField(source='sender.username', read_only=True)
    receiver = serializers.StringRelatedField(source='receiver.username', read_only=True)


    class Meta:
        model = Message
        fields = (
            'sender',
            'receiver',

        )


class ChatSerializer(serializers.ModelSerializer):

    # messages = MessageSerializer(many=True, read_only=True)
    friend = serializers.CharField()
    # last_message = serializers.CharField()

    class Meta:
        model = Chat
        fields = (
            # 'messages',
            'friend',
        )


