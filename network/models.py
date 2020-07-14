from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import Http404


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

#Q1: How do we know that our foreign key is actually on the user_id not another attribute.
#A1: When creating a table, django automatically creaties a primary id, so when referencing to that table
    #django assumes that you are refering to that primary key
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')
    content = models.CharField(max_length=1000)
    time = models.FloatField()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name="likes")
    

class Following(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name="follows")