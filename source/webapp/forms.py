from django import forms
from django.forms import widgets

from webapp.models import Article, Comment


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    author = forms.CharField(max_length=40, required=True, label='Author')
    text = forms.CharField(max_length=3000, required=True, label='Text',
                           widget=widgets.Textarea)


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=False, label='Article')
    text = forms.CharField(max_length=400, required=True, label='Text', widget=widgets.Textarea)
    author = forms.CharField(max_length=40, required=False, label='Author')
