from . import views
from django.urls import path

urlpatterns = [
    # ログインviewへのアクセス
    path('login/', views.accounts_login, name='login'),
    # ログアウトviewへのアクセス
    path('logout/', views.accounts_logout, name='logout'),
    # accounts_signup viewへのアクセスを追加しましょう。
    path('signup/', views.accounts_signup, name='signup'),
    # 問 1-13-1 accounts_signup 関数へのパスを追加しましょう。url は signup_admin/、name は signup_admin としましょう。
    path('signup_admin/',views.accounts_signup,name='signup_admin'),
]