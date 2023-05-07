from django import forms
from django.contrib.auth.forms import AuthenticationForm
# CustomUserモデルをimportする
from django.contrib.auth import get_user_model
# django の UserCreaitonForm という modelform を継承する
from django.contrib.auth.forms import UserCreationForm

# UserCreationForm を継承して SignupForm を作成する
class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        # 問 1-16-1 SignupForm クラスの fields に status を追加しましょう。
        fields = ('username', 'password1', 'password2','status')
        labels = {
            'username':'ユーザー名',
            'password1':'パスワード',
            'password2':'パスワード（確認用）',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        # 問 1-16-2 init 関数の for 文の上に statusField を hidden にする記述を追加しましょう。
        self.fields['status'].widget = forms.HiddenInput()
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

# ユーザ名とパスワードで認証するフォームを作成できる
class LoginForm(AuthenticationForm):
    # ログインフォーム
    # 会員登録フォームと同様に、全てのフォームのclass属性に「form-control」・プレースホルダーを設定する
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['style'] = 'form-control'
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        label = {
            'username':'ユーザー名',
            'password':'パスワード',
        }