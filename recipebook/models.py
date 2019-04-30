from django.db import models

from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=50)
    author_bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=15)
    instructions = models.TextField()
