from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from main.settings import HOST_NAME
from accounts.forms import UserCreationForm, UserChangeForm, UserChangePasswordForm
from accounts.models import Token


def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form':form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'])
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_active=False     #user не активный до подтверждения email
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            #токен для активации, его сложнее угадать, чем pk user
            token = Token.objects.create(user=user)
            activation_url=HOST_NAME + reverse('accounts:user_activate') + \
                            '?token={}'.format(token)
            #отправка письма на email пользователя
            user.email_user('Registration on the site localhost',
                            'To activate, follow the link: {}'.format(activation_url))
            return redirect('webapp:index')
        else:
            return render(request, 'register.html', {'form':form})



def user_activate(request):
    token_value = request.GET.get('token')
    try:
        # найти токен
        token = Token.objects.get(token=token_value)
        # активировать пользователя
        user = token.user
        user.is_active = True
        user.save()
        # удалить токен, он больше не нужен
        token.delete()
        # войти
        login(request, user)
        # редирект на главную
        return redirect('webapp:index')
    except Token.DoesNotExist:
        # если токена нет - сразу редирект
        return redirect('webapp:index')

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_obj'
    form_class = UserChangeForm

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_change_password.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:login')


#
# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             next_url = request.POST.get('next')
#             if next_url:
#                 return redirect(next_url)
#             return redirect('webapp:index')
#         else:
#             context['has_error'] = True
#     else:
#         context['next'] = request.GET.get('next', '')
#     return render(request, 'login.html', context=context)
#
#
# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('webapp:index')

