from django.contrib.auth.hashers import make_password
from faker import Faker
from account.models import User

fake = Faker()

def run():
  user_data = [
    {
      'email': 'user1@dummy.com',
      'name': fake.name(),
      'password1': 'today123',
    },
    {
      'email': 'user2@dummy.com',
      'name': fake.name(),
      'password1': 'today123',
    },
    {
      'email': 'user3@dummy.com',
      'name': fake.name(),
      'password1': 'today123',
    },
    {
      'email': 'user4@dummy.com',
      'name': fake.name(),
      'password1': 'today123',
    },
    {
      'email': 'user5@dummy.com',
      'name': fake.name(),
      'password1': 'today123',
    }
  ]

  User.objects.bulk_create([
    User(
      email=data['email'],
      name=data['name'],
      password=make_password(data['password1'])
    )
    for data in user_data
  ])

  emails = [data['email'] for data in user_data]
  users = User.objects.filter(email__in=emails)

  for user in users:
    for other in users:
      if other != user:
        user.friends.add(other)
        user.friends_count = user.friends_count + 1
        user.save()

  for user in users:
    print(f"User: {user.email}, Friends: {[friend.email for friend in user.friends.all()]}")
