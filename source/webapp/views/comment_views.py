from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import CommentForm
from webapp.models import Comment


class CommentIndexView(TemplateView):
    template_name = 'comments/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        return context


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comments/create.html', context={'form': form})
    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment = Comment.objects.create(
            article = form.cleaned_data['article'],
            text = form.cleaned_data['text']
            )
            return redirect('comment_index')
        else:
            return render(request, 'comments/create.html', context={'form': form})


class CommentEditView(View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = CommentForm(data={
            'text': comment.text,
            'author': comment.author
            })
        return render(request, 'comments/update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        if form.is_valid():
            data = form.cleaned_data
            comment.text = data['text']
            comment.author = data['author']
            comment.save()
            return redirect('comment_index')
        else:
            return render(request, 'comments/update.html', context={'form': form, 'comment': comment})


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        return render(request, 'comments/delete.html', context={'comment': comment})

    def post(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('comment_index')