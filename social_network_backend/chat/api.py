from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer

@api_view(['GET'])
def conversation_list(req):
  conversations = Conversation.objects.filter(users__in=list([req.user]))

  if conversations:
    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse([], safe=False)

@api_view(['GET'])
def conversation_detail(req, pk):
  conversation = Conversation.objects.filter(users__in=list([req.user])).get(pk=pk)
  serializer = ConversationDetailSerializer(conversation)

  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(req, user_pk):
  user = User.objects.get(pk=user_pk)

  conversations = Conversation.objects.filter(users__in=list([req.user])).filter(users__in=list([user]))

  if conversations:
    conversation = conversations.first()
  else:
    conversation = Conversation.objects.create()
    conversation.users.add(user, req.user)
    conversation.save()

  serializer = ConversationDetailSerializer(conversation)

  return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def conversation_send_message(req, pk):
  conversation = Conversation.objects.filter(users__in=list([req.user])).get(pk=pk)

  for user in conversation.users.all():
    if user != req.user:
      sent_to = user

  conversation_message = ConversationMessage.objects.create(
    conversation=conversation,
    body=req.data.get('body'),
    created_by=req.user,
    sent_to=sent_to
  )

  serializer = ConversationMessageSerializer(conversation_message)

  return JsonResponse(serializer.data, safe=False)