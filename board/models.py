from django.db import models

class Posts(models.Model):
    is_seen = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)
    image = models.ImageField(upload_to = "board/", default='board/image.gif') #default 수정 필요
    body = models.TextField()
    category = models.CharField(max_length=10)
    comments_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    liked_users = models.TextField(default="None,", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def summary(self):
        if len(self.title) >= 10:
            return self.title[:10] + "..."
        else:
            return self.title