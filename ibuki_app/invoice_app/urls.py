from django.urls import path
from . import views
from .views import Client_modify
# 「views.py」をインポート
urlpatterns = [
    # path(URL, 紐付ける関数, ページ名)
    path('', views.main, name='main'),
    path('client_add/', views.client_add, name='client_add'),
    path('input/', views.input, name='input'),
    path('actual_list',views.service_record_list,name='actual_list'),
    path('record_list_modify/<int:pk>/',views.record_list_modify,name='record_list_modify'),
    path('a_edit/<int:actual_id>',views.actual_edit,name='actual_edit'),
    path('actual_bulk_edit',views.actual_bulk_edit,name='actual_bulk_edit'),
    path('a_delete/<int:actual_id>',views.actual_delete,name='actual_delete'),
    path('client_list',views.client_list,name='client_list'),
    path('modify/<int:pk>/',Client_modify.as_view(),name='client_modify'),
    path('delete/<int:client_id>',views.Client_delete,name='client_delete'),
    path('test',views.main,name='test'),
    path('invoices/<int:year>/<int:month>/',views.view_invoices_for_month),
]
