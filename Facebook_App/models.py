from django.db import models

class Post(models.Model):
    post_id = models.CharField(max_length=255)
    message = models.TextField()
    likes = models.IntegerField()
    comments = models.IntegerField()
    shares = models.IntegerField()
    url = models.TextField()