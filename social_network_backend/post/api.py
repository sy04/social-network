from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm, PostListParams
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer

from account.models import FriendshipRequest

@api_view(['GET'])
def post_list(req):
    params = PostListParams(
      page=int(req.GET.get('page', 1)),
      limit=int(req.GET.get('limit', 10))
    )

    user_ids = [req.user.id]

    for user in req.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = req.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    paginator = PageNumberPagination()
    paginator.page = params.page
    paginator.page_size = params.limit
    paginate_posts = paginator.paginate_queryset(posts, req)  # Provide the request object here

    count = posts.count()
    page_count = paginator.page.paginator.num_pages

    sl_no = 0 if paginator.page.number == 1 else (paginator.page.number - 1) * paginator.page_size

    paginator_data = {
        'itemCount': count,
        'limit': paginator.page_size,
        'pageCount': page_count,
        'page': paginator.page.number,
        'slNo': sl_no + 1,
        'hasPrevPage': paginator.page.has_previous(),
        'hasNextPage': paginator.page.has_next(),
        'prevPage': paginator.page.previous_page_number() if paginator.page.has_previous() else None,
        'nextPage': paginator.page.next_page_number() if paginator.page.has_next() else None,
    }

    serializer = PostSerializer(paginate_posts, many=True)

    result = {
        'posts': serializer.data if count > 0 else [],
        'paginator': paginator_data
    }

    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_detail(req, pk):
  user_ids = [req.user.id]

  for user in req.user.friends.all():
    user_ids.append(user.id)

  post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

  return JsonResponse({
    'post': PostDetailSerializer(post).data
  })

@api_view(['GET'])
def post_list_profile(req, id):
  user = User.objects.get(pk=id)
  posts = Post.objects.filter(created_by_id=id)

  if not req.user in user.friends.all():
    posts = posts.filter(is_private=False)

  post_serialiazer = PostSerializer(posts, many=True)
  user_serialiazer = UserSerializer(user)

  cant_send_friendship_request = True

  if req.user in user.friends.all():
    cant_send_friendship_request = False

  check1 = FriendshipRequest.objects.filter(created_for=req.user).filter(created_by=user)
  check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=req.user)

  if check1 or check2:
    cant_send_friendship_request = False

  return JsonResponse({
      'posts': post_serialiazer.data,
      'user': user_serialiazer.data,
      'cant_send_friendship_request': cant_send_friendship_request
    }, safe=False)

@api_view(['POST'])
def post_create(req):
  form = PostForm(req.data)
  attachment = None
  attachment_form = AttachmentForm(req.POST, req.FILES)

  if attachment_form.is_valid():
    attachment = attachment_form.save(commit=False)
    attachment.created_by = req.user
    attachment.save()

  if form.is_valid():
    post = form.save(commit=False)
    post.created_by = req.user
    post.save()

    if attachment:
      post.attachment.add(attachment)

    user = req.user
    user.posts_count = user.posts_count + 1
    user.save()

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

  if post.created_by != req.user:
    notification = create_notification(req, 'post_like', post_id=post.id)

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

  if post.created_by != req.user:
    notification = create_notification(req, 'post_comment', post_id=post.id)

  serializer = CommentSerializer(comment)

  return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def post_delete(req, pk):
  post = Post.objects.filter(created_by=req.user).get(pk=pk)
  post.delete()

  user = req.user
  user.posts_count = user.posts_count - 1
  user.save()

  return JsonResponse({'message': 'post deleted'})

@api_view(['POST'])
def post_report(req, pk):
  post = Post.objects.get(pk=pk)
  post.reported_by_users.add(req.user)
  post.save()

  return JsonResponse({'message': 'post reported'})

@api_view(['GET'])
def get_trends(req):
  serializer = TrendSerializer(Trend.objects.all(), many=True)

  return JsonResponse(serializer.data, safe=False)