from django.shortcuts import render

from rest_framework import generics
from django.db.models import Q, Count, Prefetch, F, Case, When, Subquery, OuterRef, Max

from chat import models

from chat import serializers


class  ChatListAPI(generics.ListAPIView):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(messages__sender__in=[self.request.user]) |
            Q(messages__receiver__in=[self.request.user])
        ).annotate(
            friend=F('messages__receiver__username'))

        return queryset


"""
.select_related(
            'sender', 'receiver'
        )
        queryset = queryset.filter(
            Q(sender__in=[self.request.user]) | Q(receiver__in=[self.request.user])
        ).annotate(
            receiver_count=Count(
                'pk', filter=~Q(sender__in=[self.request.user])
            )
        )

"""
