from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(to='User')


class Post(models.Model):
    text = models.TextField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="post_owner")
    likes = models.ManyToManyField(to=User, related_name="user_like")
