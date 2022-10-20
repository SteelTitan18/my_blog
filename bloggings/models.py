from django.db import models
from django.contrib.auth.models import User

class Theme(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.label

class Post(models.Model):
    title = models.CharField(verbose_name="Titre ", max_length=50)
    content = models.TextField(verbose_name="Contenu ", unique=True)
    theme = models.ForeignKey(Theme, verbose_name="Thème ", on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addHour = models.TimeField(auto_now=True, auto_now_add=False)
    modifHour = models.TimeField(auto_now=False, auto_now_add=True)
    addDate = models.DateField(auto_now=True, auto_now_add=False)
    modifDate = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Commentaire ", unique=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    addHour = models.TimeField(auto_now=True, auto_now_add=False)
    addDate = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.content
