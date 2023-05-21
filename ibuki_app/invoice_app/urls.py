from django.urls import path
from .views import Client_modify,Client_delete
# 「views.py」をインポート
from . import views
urlpatterns = [
    # path(URL, 紐付ける関数, ページ名)
    path('', views.main, name='main'),
    path('client_add/', views.client_add, name='client_add'),
    path('input/', views.input, name='input'),
    path('actual_list',views.actual_list,name='actual_list'),
    path('actual_list',views.actual_bulk_edit,name='actual_bulk_edit'),
    path('actual_edit/<int:actual_id>',views.actual_edit,name='actual_edit'),
    path('a_delete/<int:actual_id>',views.actual_delete,name='actual_delete'),
    path('client_list',views.client_list,name='client_list'),
    path('modify/<int:pk>/',Client_modify.as_view(),name='client_modify'),
    path('delete/<int:client_id>',views.Client_delete,name='client_delete'),
]
