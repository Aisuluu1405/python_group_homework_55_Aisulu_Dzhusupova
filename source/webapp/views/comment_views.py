from django.shortcuts import  get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from webapp.forms import CommentForm, ArticleCommentForm
from webapp.models import Comment, Article


class CommentIndexView(ListView):
    template_name = 'comments/index.html'
    context_object_name = 'comments'
    model = Comment
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1


class CommentForArticleCreateView(CreateView):
    template_name = 'comments/create.html'
    form_class = ArticleCommentForm

    def form_valid(self, form):
        article_pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        article.comments.create(**form.cleaned_data)
        return redirect('article_view', pk=article_pk)


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('comment_index')


class CommentEditView(UpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('article_view')


class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('comment_index')
