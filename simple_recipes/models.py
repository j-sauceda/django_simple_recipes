from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    categories = models.ManyToManyField(Category,
                                        related_name='categoryOf',
                                        blank=True)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)

    class Meta:
        ordering = ['-date']

    def abstract(self):
        return str(self.body)[0:200] + "..."

    def __str__(self):
        return self.title + ', by ' + str(self.author)


class ArticlePicture(models.Model):
    article = models.ForeignKey(Article,
                                related_name='pictureOf',
                                on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article,
                                related_name='commentOf',
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    commentor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.commentor) + ' said: ' + self.text[0:50]
