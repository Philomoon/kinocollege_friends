from django.urls import path
# 「views.py」をインポート
from . import views
urlpatterns = [
    # path(URL, 紐付ける関数, ページ名)
    path('', views.main, name='main'),
    path('client_add/', views.client_add, name='client_add'),
    path('input/', views.input, name='input'),
]
