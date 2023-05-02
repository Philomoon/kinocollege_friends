from django.urls import path
from . import views

urlpatterns = [
    # ホーム画面
    path('',views.home,name='home'),
    # ログアウト
    path('logout/',views.Logout.as_view(),name='logout'),
    # 商品一覧
    path('product_list/',views.product_list,name='product_list'),
    # カートの中
    path('mycart/',views.mycart,name='mycart'),
    # カートの商品を削除する
    path('delete/',views.delete,name='delete'),
    # 商品詳細
    path('product_detail/<int:num>',views.product_detail,name='product_detail'),
    # ajaxのカート追加機能
    path('add_cart/',views.add_cart,name='add_cart'),
    # ajaxのカート削除機能
    path('delete/',views.delete,name='delete'),
    # qty書き換え
    path('change_qty', views.change_qty, name='change_qty'),
    # 購入履歴
    path('purchase_history', views.purchase_history, name='purchase_history'),
    # 問 2-6-1 admin_register_product 関数へのパスを追加しましょう。url は admin_register_product/、name は admin_register_product としましょう。

    # 問 3-6-1 admin_product_list 関数へのパスを追加しましょう。url は admin_product_list/、name は admin_product_list としましょう。

    # 問 4-6-1 search_product 関数へのパスを追加しましょう。url は search_product/、name は search_product としましょう。

    ]
