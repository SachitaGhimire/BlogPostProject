from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from tinymce.models import HTMLField

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = HTMLField()
    image = models.URLField(null=True)
    # image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
       

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    twitter = models.CharField(max_length=300, blank=True, null=True)
    github = models.CharField(max_length=300, blank=True, null=True)


    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment



