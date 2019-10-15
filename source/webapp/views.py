from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from webapp.models import Article


class ArticleIndexView(TemplateView):
    template_name = 'article/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context

