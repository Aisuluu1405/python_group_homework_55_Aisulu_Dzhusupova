from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Article, Comment


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length =50, required=False)

    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) <= 0 or isinstance(tags, str) and tags == '' or '  ' in tags:
            raise ValidationError("You have an empty 'tags' field.")
        return tags.split(',')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label="To the text")
    in_title = forms.BooleanField(initial=True, required=False, label='In the title')
    in_text = forms.BooleanField(initial=True, required=False, label='In the text')
    in_tags = forms.BooleanField(initial=True, required=False, label='In the tags')
    in_comment_text = forms.BooleanField(initial=False, required=False, label='In the comments')

    author = forms.CharField(max_length=100, required=False, label="By author")
    article_author = forms.BooleanField(initial=True, required=False, label='Articles')
    comment_author = forms.BooleanField(initial=False, required=False, label='Comments')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        if not data.get('text') and not data.get('author'):
            raise ValidationError(
                '*Field "text" or "author" should not be empty!',
                code='text_author_search_criteria_empty'
            )
        errors = []
        if data.get('text'):
            if not (data.get('in_title') or data.get('in_text')
                    or data.get('in_tags') or data.get('in_comment_text')):
                raise ValidationError(
                    errors.append(ValidationError(
                        '*One of the following checkboxes should be checked: In title, In text, In tags, In comment text!',
                        code='text_search_criteria_empty')
                ))
        if data.get('author'):
            if not (data.get('article_author') or data.get('comment_author')):
                errors.append(ValidationError(
                   '*One of the following checkboxes should be checked: Article_author, Comment_author!',
                    code='author_search_criteria_empty'
                ))
        if errors:
            raise ValidationError(errors)
        return data


