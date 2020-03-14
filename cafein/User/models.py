from django.db import models

# ここから追加
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone


# cloudinaryを使う上で必須
import cloudinary

import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField



'''
UserManager とは
->Django の User モデルの管理に必要なクラスのこと。例えば User を作成するためのメソッドなどを管理している
これは Django のモデルを扱うクラスも継承しており、Userモデルの中の objects という変数で管理している

BaseUserManager
->create_user や create_superuser などの関数が定義されており、それらをオーバーライドすることによって username ではなく email での登録をするようにしている

use_in_migrations = True
->このクラスもマイグレーションで管理できるようになる

normalize_email
-> メールアドレスのドメイン部分を小文字にして電子メールアドレスを正規化する
'''
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # email を必須にする
        if not email:
            raise ValueError('メールアドレスを入れてください')
        # email で User モデルを作成
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)




'''
PermissionsMixin
->管理者権限周りの機能を追加してくれるクラス。カスタムユーザー作成の際は必須

unique = True
->他のユーザーと被りが出ないようにする

USERNAME_FIELD = 'email'
->email というフィールド でこのプロジェクトの User を一意に判別するという設定ができる
つまり、このフィールド(今回は email)の情報でユーザーを検索すれば、必ず一人のユーザーだけが結果として表示される

REQUIRED_FIELDS = []
->createsuperuserを行うときに必須となるフィールドを指定できまる
しかし、USERNAME_FIELD と password のフィールドについては必ず必須になるので、こちらで指定する必要はない
'''
class User(AbstractBaseUser, PermissionsMixin):
    good_name = models.CharField('ユーザーネーム', max_length=30, unique=True)
    email = models.EmailField('メールアドレス', unique=True)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    user_description = models.TextField('自己紹介文', blank=True, null=True)
    user_img = models.ImageField('プロフィール画像', upload_to='user_img', default=None)
    # user_img = CloudinaryField('user_img', blank=True, null=True)
    date_joined = models.DateTimeField('date_joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['good_name',]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'