import os

from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from notification.utils import create_notification
from .forms import SignupForms, ProfileForms
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer

@api_view(['GET'])
def me(req):
  return JsonResponse({
    'id': req.user.id,
    'name': req.user.name,
    'email': req.user.email,
    'avatar': req.user.get_avatar()
  })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(req):
  data = req.data
  message = 'success'

  form = SignupForms({
    'email': data.get('email'),
    'name': data.get('name'),
    'password1': data.get('password1'),
    'password2': data.get('password2'),
  })

  if form.is_valid():
    user = form.save()
    user.is_active = False
    user.save()

    url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'

    send_mail(
      "Please verify your email",
      f"The url for activatinf your account is: {url}",
      "noreply@harakirimail.com",
      [user.email],
      fail_silently=False
    )

  else:
    message = form.errors

  return JsonResponse({'message': message}, safe=False)

@api_view(['GET'])
def friends(req, pk):
  user = User.objects.get(pk=pk)
  requests = []

  if user == req.user:
    requests = FriendshipRequest.objects.filter(created_for=req.user, status=FriendshipRequest.SENT)
    requests = FriendshipRequestSerializer(requests, many=True)
    requests = requests.data

  friends = user.friends.all()

  return JsonResponse({
    'user': UserSerializer(user).data,
    'friends': UserSerializer(friends, many=True).data,
    'requests': requests
  },  safe=False)

@api_view(['GET'])
def my_friendship_suggestions(req):
  serializer = UserSerializer(req.user.people_may_you_know.all(), many=True)

  return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def editprofile(req):
  user = req.user
  email = req.data.get('email')

  if User.objects.exclude(id=user.id).filter(email=email).exists():
    return JsonResponse({'message': 'email already exists'})
  else:
    form = ProfileForms(req.POST, req.FILES, instance=user)
    old_avatar_path = user.avatar.path if user.avatar else None

    if form.is_valid():
      form.save()

      if old_avatar_path and user.avatar and old_avatar_path != user.avatar.path:
        if os.path.exists(old_avatar_path):
          os.remove(old_avatar_path)

    serializer = UserSerializer(user)

    return JsonResponse({
      'message': 'information updated',
      'user': serializer.data
    })

@api_view(['POST'])
def editpassword(req):
  user = req.user
  form = PasswordChangeForm(data=req.POST, user=user)

  if form.is_valid():
    form.save()

    return JsonResponse({'message': 'success'})
  else:
    return JsonResponse({'message': form.errors}, safe=False)

@api_view(['POST'])
def send_friendship_request(req, pk):
  user = User.objects.get(pk=pk)

  check1 = FriendshipRequest.objects.filter(created_for=req.user).filter(created_by=user)
  check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=req.user)

  if not check1 and not check2:
    friendrequest = FriendshipRequest.objects.create(created_for = user, created_by = req.user)

    notification = create_notification(req, 'new_friendrequest', friendrequest_id=friendrequest.id)

    return JsonResponse({'message': 'friendship request created'})
  else:
    return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_request(req, pk, status):
  user = User.objects.get(pk=pk)
  friendship_request = FriendshipRequest.objects.filter(created_for=req.user).get(created_by=user)
  friendship_request.status = status
  friendship_request.save()

  if status == 'accepted':
    user.friends.add(req.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = req.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    notification = create_notification(req, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

  return JsonResponse({'message': 'friendship request updated'})