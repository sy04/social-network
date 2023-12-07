from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .forms import PostForm
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer

@api_view(['GET'])
def post_list(req):
  user_ids = [req.user.id]

  for user in req.user.friends.all():
    user_ids.append(user.id)

  posts = Post.objects.filter(created_by_id__in=list(user_ids))
  trend = req.GET.get('trend', '')

  if trend:
    posts = posts.filter(body__icontains='#' + trend)

  serializer = PostSerializer(posts, many=True)

  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(req, pk):
  post = Post.objects.get(pk=pk)

  return JsonResponse({
    'post': PostDetailSerializer(post).data
  })

@api_view(['GET'])
def post_list_profile(req, id):
  user = User.objects.get(pk=id)
  posts = Post.objects.filter(created_by_id=id)

  post_serialiazer = PostSerializer(posts, many=True)
  user_serialiazer = UserSerializer(user)

  return JsonResponse({
      'posts': post_serialiazer.data,
      'user': user_serialiazer.data
    }, safe=False)

@api_view(['POST'])
def post_create(req):
  form = PostForm(req.data)

  if form.is_valid():
    post = form.save(commit=False)
    post.created_by = req.user
    post.save()

    serializer = PostSerializer(post)

    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse({'error': 'add something here later! ...'})

@api_view(['POST'])
def post_like(req, pk):
  post = Post.objects.get(pk=pk)

  if not post.likes.filter(created_by=req.user):
    like = Like.objects.create(created_by=req.user)

    post = Post.objects.get(pk=pk)
    post.likes_count = post.likes_count + 1
    post.likes.add(like)
    post.save()

    return JsonResponse({'message': 'like created'})
  else:
    return JsonResponse({'message': 'post already liked'})

@api_view(['POST'])
def post_create_comment(req, pk):
  comment = Comment.objects.create(body=req.data.get('body'), created_by=req.user)

  post = Post.objects.get(pk=pk)
  post.comments.add(comment)
  post.comments_count = post.comments_count + 1
  post.save()

  serializer = CommentSerializer(comment)

  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_trends(req):
  serializer = TrendSerializer(Trend.objects.all(), many=True)

  return JsonResponse(serializer.data, safe=False)