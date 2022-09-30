from django.contrib import admin
from .models import Article, ArticleComment, ArticlePicture, Category, Profile


# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(ArticlePicture)
admin.site.register(Category)
admin.site.register(Profile)