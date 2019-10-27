from django.urls import path

from webapp.views import ArticleIndexView, ArticleView, ArticleCreateView, ArticleEditView, ArticleDeleteView,\
    CommentIndexView, CommentCreateView, CommentEditView, CommentDeleteView, CommentForArticleCreateView,\
    ArticleSearchView

app_name = 'webapp'

urlpatterns = [
    path('', ArticleIndexView.as_view(), name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/edit/', ArticleEditView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/search/', ArticleSearchView.as_view(), name='article_search'),
    path('comment/', CommentIndexView.as_view(), name='comment_index'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:pk>/edit/', CommentEditView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('article/<int:pk>/add-comment/', CommentForArticleCreateView.as_view(), name='article_comment_add'),
# path('search/result/', ResultView.as_view(), name ='result')
]

