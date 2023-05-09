from django.db import models
# AbstractUser を継承してカスタムユーザーを作成するためにインポート
from django.contrib.auth.models import AbstractUser
# 認証に使うユーザーモデルを setting.py から取得するためのメソッド
from django.contrib.auth import get_user_model
# models に適用させるvalidator
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
  first_name = None
  last_name = None
  last_login = None
  # 問 1-5-1 CustomUser クラスに status フィールドを追加しましょう。種類は IntegerField で、default=1 を設定しましょう。
  status = models.IntegerField(default=1)

  def __str__(self):
    return self.username