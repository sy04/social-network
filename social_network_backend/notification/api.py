from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notifications(req):
  received_notifications = req.user.received_notifications.filter(is_read=False)
  serializer = NotificationSerializer(received_notifications, many=True)

  return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notification(req, pk):
  notification = Notification.objects.filter(created_for=req.user).get(pk=pk)
  notification.is_read = True
  notification.save()

  return JsonResponse({'message': 'notification read'})