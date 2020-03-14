from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User


class MyUserChangeForm(UserChangeForm):
    """User 情報を変更するフォーム"""
    class Meta:
        model = User

        # __all__ があることによって全ての情報を変更可能
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    """User を作成するフォーム"""
    class Meta:
        model = User
    
        # emailとgood_name(username)とパスワード(デフォルト)が必要
        fields = ('email', 'good_name',)


class MyUserAdmin(UserAdmin):

    # ここに書いてあるものは後から追加できる情報
    fieldsets = (
        (None, {'fields': ('email', 'user_description','password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff','is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('email', 'password1', 'password2'),}),
    )


    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('good_name', 'email', 'user_description','is_staff', 'is_active', )
    # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, MyUserAdmin)