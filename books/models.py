from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_group = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    file_url = models.URLField(help_text="Paste raw GitHub URL to the PDF")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class ReadingExercise(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title
