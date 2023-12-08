from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

def create_notification(req, type_of_notification, post_id=None, friendrequest_id=None):
  created_for = None

  if type_of_notification == 'post_like':
    body = f'{req.user.name} liked one of your posts!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'post_comment':
    body = f'{req.user.name} commended on one of your posts!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'new_friendrequest':
    friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    created_for = friendrequest.created_for
    body = f'{req.user.name} sent you a friend request!'
  elif type_of_notification == 'accepted_friendrequest':
    friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    created_for = friendrequest.created_by
    body = f'{req.user.name} accepted you a friend request!'
  elif type_of_notification == 'rejected_friendrequest':
    friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    created_for = friendrequest.created_by
    body = f'{req.user.name} rejected you a friend request!'

  notification = Notification.objects.create(
    body=body,
    type_of_notification=type_of_notification,
    created_by=req.user,
    post_id=post_id,
    created_for=created_for
  )

  return notification