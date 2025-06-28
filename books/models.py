from django.db import models
from django.contrib.auth.models import User
from pyuploadcare.dj.models import FileField

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_group = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    file_url = models.URLField()
    file_uuid = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_view_url(self):
        return f"https://ucarecdn.com/{self.file_uuid}/"

    def get_download_url(self):
        return f"https://ucarecdn.com/{self.file_uuid}/?dl="


class ReadingExercise(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title
