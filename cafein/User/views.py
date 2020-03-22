from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.urls import reverse_lazy



'''
forms.pyで作成したCustomUserCreationFormを使って新しいユーザーを作成していく。
フォームの入力データからemailとpassword1の値を取り出し、authenticate関数でユーザーの認証をとっている。認証がうまくいった際には、ユーザーをそのままログインさせてトップページにリダイレクトする処理になっています。
'''

def signup(request):
    if request.user.is_authenticated:
        return redirect('post:login')
    if request.method == 'POST':
        # ユーザーインスタンスを作成
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # ユーザーインスタンスを保存
            new_user = form.save()
            input_username = form.cleaned_data['good_name']
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければ None を返す
            new_user = authenticate(email=input_email, good_name=input_username, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('main:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


# 関数名を logout にしてしまうとエラーとなる(デフォルトで logout が用意されているため)
def logout_func(request):
    logout(request)
    messages.info(request, 'ログアウトしました')
    return redirect('home:home')


class EditProfile(UpdateView, LoginRequiredMixin):
    template_name = 'user/edit.html'
    model = User
    fields = ('email', 'good_name', 'user_description', 'user_img')
    success_url = reverse_lazy('main:profile')

    # fields = ('email', 'good_name', 'user_description', 'user_img')