from django.contrib.auth.mixins import LoginRequiredMixin
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


class CommentForArticleCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = ArticleCommentForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_article()
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.article = self.article
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def form_valid(self, form):
        self.article.comments.create(
            author=self.request.user,
            **form.cleaned_data
        )
        return redirect('webapp:article_view', pk=self.article.pk)

    def get_article(self):
        article_pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=article_pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comments/create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:comment_index')


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comments/update.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('webapp:article_view')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:comment_index')
