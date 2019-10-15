from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
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


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'article/create.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            article = Article.objects.create(
                title=data['title'],
                author=data['author'],
                text=data['text'],
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/create.html', context={'form': form})

class ArticleEditView(View):
    def get(self, request, *args, **kwargs):
        article_pk= kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = ArticleForm(data={
            'title': article.title,
            'author': article.author,
            'text': article.text,
            })
        return render(request, 'article/update.html', context={'form': form, 'article': article})
    def post(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            article.title = data['title']
            article.author = data['author']
            article.text = data['text']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article/update.html', context={'form': form, 'article': article})
