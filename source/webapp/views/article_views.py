from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from webapp.forms import ArticleForm, ArticleCommentForm
from webapp.models import Article


class ArticleIndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    model = Article
    ordering = ['-created_at']
    paginate_by = 4
    paginate_orphans = 1


class ArticleView(DetailView):
    template_name = 'article/article.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleCommentForm()
        comments = context['article'].comments.order_by('-created_at')
        self.paginate_comments_to_context(comments, context)
        return context

    def paginate_comments_to_context(self, comments, context):
        paginator = Paginator(comments, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()



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


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        return render(request, 'article/delete.html', context={'article': article})
    def post(self, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
        return redirect('index')

