from django.urls import path
from accounts.views import login_view, logout_view, register_view, user_activate, UserDetailView, UserChangeView

app_name = 'accounts'

urlpatterns =[
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/activate/', user_activate, name='user_activate'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile<pk>/edit/', UserChangeView.as_view(), name='user_update')


]
