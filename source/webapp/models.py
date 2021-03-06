from django.contrib.auth.models import User
from django.db import models


def get_admin():
    return User.objects.get(username='admin').id


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Title')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Text')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles', null=False, blank=False,
                               default=get_admin, verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Change time')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Category',
                                 related_name='articles')
    tags = models.ManyToManyField('webapp.Tag', related_name='articles', blank=True, verbose_name='Tags')

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='comments',
                                on_delete=models.CASCADE, verbose_name='Article')
    text = models.TextField(max_length=400, verbose_name='Comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',null=True, blank=True, default=None, verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Change time')

    def __str__(self):
        return self.text[:20]


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Tag')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date create')

    def __str__(self):
        return self.name