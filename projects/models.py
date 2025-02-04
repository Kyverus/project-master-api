from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
