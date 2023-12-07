from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForms, ProfileForms
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer

@api_view(['GET'])
def me(req):
  return JsonResponse({
    'id': req.user.id,
    'name': req.user.name,
    'email': req.user.email
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
    form.save()
  else:
    message = 'error'

  return JsonResponse({'message': message})

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

@api_view(['POST'])
def editprofile(req):
  user = req.user
  email = req.data.get('email')

  if User.objects.exclude(id=user.id).filter(email=email).exists():
    return JsonResponse({'message': 'email already exists'})
  else:
    form = ProfileForms(req.data, instance=user)

    if form.is_valid():
      form.save()

    return JsonResponse({'message': 'information updated'})

@api_view(['POST'])
def send_friendship_request(req, pk):
  user = User.objects.get(pk=pk)

  check1 = FriendshipRequest.objects.filter(created_for=req.user).filter(created_by=user)
  check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=req.user)

  if not check1 and not check2:
    FriendshipRequest.objects.create(created_for = user, created_by = req.user)
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

  return JsonResponse({'message': 'friendship request updated'})