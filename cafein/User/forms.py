from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# cloudinary使うなら必須
from cloudinary.forms import CloudinaryFileField

'''
DjangoのデフォルトのUserモデルを利用する場合は付属のUserCreationFormをそのまま使うだけでサインアップ用のフォームを作ることができた。
しかし、今回はカスタムユーザーモデルを作成しているため、新しく設定したフィールドに合わせてユーザー作成のフォームを作る必要がある。これを実現するために、UserCreationForm をオーバーライドした CustomUserCreationFormクラスを作成し、サインアップページを作っていく。
-------------------------------------------------------------------------------------------
デフォルトのUserモデルの場合、django.contrib.auth.models.Userをインポートすることになるが、今回はカスタムユーザーモデルを参照する必要がある。

カスタムユーザーモデルを参照するには get_user_model 関数を使う。この関数ではsettings.pyのAUTH_USER_MODEL(今回はUser.User)に設定したモデルを呼び出す。カスタムユーザーを使っている場合、どのファイルからもこちらの関数を利用することでUserモデルを呼び出すことができるので覚えておく。
'''


class CustomUserCreationForm(UserCreationForm):
    # user_img = CloudinaryFileField(
    #         options={'folder': 'media/user_img', 'tags': 'User'})
    
    class Meta:
        model = get_user_model()
        fields = ('email','good_name',)