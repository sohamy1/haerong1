from django.db import models

class Comments(models.Model):
    linked_post = models.IntegerField()
    writer = models.CharField(max_length=50)
    body = models.TextField()
    stars = models.IntegerField(default=0)
    liked_users = models.TextField(default="None,", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)