from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Product, Order
from django.http import JsonResponse ,HttpResponse
from django.contrib.auth.views import LogoutView
import datetime
# 問 2-5-3-1 RegisterForm を ec_app/forms.py からインポートしましょう。
# 問 4-5-4 ec_app/forms.py から SearchProductForm をインポートしましょう。

# 問 4-5-3-6 Q オブジェクトを django.db.models からインポートしましょう。


# ホーム
def home(request):
    # 問 1-15-1-1 ログインユーザーの status を status 変数に格納しましょう。
<<<<<<< HEAD
<<<<<<< HEAD
    status = request.status
    # 問 1-15-1-2 render メソッドの第三引数で、キー：status、バリュー：status として渡しましょう。
    return render(request,'ec_app/home.html',status='status')
=======
=======
>>>>>>> 9873cb210f669ff508d6663d34ad743cc65e8df6
    status = request.user.status

    # 問 1-15-1-2 render メソッドの第三引数で、キー：status、バリュー：status として渡しましょう。
    return render(request,'ec_app/home.html',status=status)
<<<<<<< HEAD
>>>>>>> philo
=======
>>>>>>> 9873cb210f669ff508d6663d34ad743cc65e8df6

# ログアウト
class Logout(LogoutView):
    template_name = 'ec_app/logout.html'

# 商品一覧画面
def product_list(request):
    # 商品情報を取得
    products = Product.objects.all()
    # 問 5-2-1 products 変数に、get_dict 関数の戻り値を際代入しましょう。引数は products を指定しましょう。

    # 問 5-2-2 products 変数の下に、pickups 変数を空のリストで定義しましょう。

    # 問 5-2-3 for 文で products を回しましょう。サンプルコードを追加しましょう。

        # 問 5-2-4 for 文に pickupsが 3 以下の時という条件式を追加しましょう。リストの要素数は len で取得できます。

            # 問 5-2-5 条件式の中に、更新日と本日の日付が3日以内の時、という条件式を追加しましょう。

                # 問 5-2-6 True だった際に、products 変数から pop して、返り値を pickup リストに追加しましょう。

    # 問 5-2-7 params にキー；pickups、バリュー：pickups を指定しましょう。
    params = {
        'products':products,
        'title':'商品一覧',

    }
    return render(request,'ec_app/product_list.html',params)

# カート画面
def mycart(request):
    params = {}
    if request.method == 'POST':
        # 注文ボタンを押したら、doneをTrueに、ordered_atを本日の日付を格納する
        orders = Order.objects.filter(user=request.user, done=False)
        if orders.exists():
            for order in orders:
                order.ordered_at = datetime.datetime.now()
                order.done = True
                order.save()
                params['succece'] = 'ご注文ありがとうございます。到着まで今しばらくお待ちください。'
    # 決済が完了していない自分のカート情報を取得
    params['mycart'] = Order.objects.filter(user=request.user).filter(done=False)
    return render(request,'ec_app/mycart.html',params)

# 商品詳細画面
def product_detail(request,num):
    # 押された商品のレコードを取得する
    target = Product.objects.get(pk=num)
    params = {
        'target':target,
    }
    return render(request,'ec_app/product_detail.html',params)

def add_cart(request):
    if request.method == 'POST':
        # ajaxで送られてきたidをid変数に格納
        id = request.POST.get('id')
        # idから商品情報取得
        product = Product.objects.get(pk=id)
        user = request.user
        # もし、注文レコードが存在する場合
        if Order.objects.filter(product=product,user=user,done=False).exists():
            # # 存在する場合は該当レコードのqtyを+1する
            order = Order.objects.get(product=product,user=user,done=False)
            order.qty += 1
            order.save()
        else:
            # 新規レコードを作成する
            new_order = Order()
            new_order.user = user
            new_order.product = product
            new_order.qty = 1
            new_order.save()
        data = {
            'msg':f'{product.product_name}をカートに追加しました。',
        }
        return JsonResponse(data)

# order削除機能
def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        order = Order.objects.get(pk=id)
        order.delete()
        msg = 'カートから削除しました。'
        boo = True
    else:
        msg = '問題が発生しました。'
        boo = False
    params = {
        'msg':msg,
        'boo':boo,
    }
    return JsonResponse(params)

# 購入履歴
def purchase_history(request):
    params = {}
    if request.method == 'POST':
        # 注文IDを取得
        id = request.POST.get('id')
        # インスタンスを作成して、新たにレコードを作成する
        if Order.objects.filter(user=request.user, done=False).exists():
            order = Order.objects.filter(user=request.user, done=False)
        else:
            order = Order()
        order.qty = Order.objects.get(pk=id).qty
        order.done = False
        order.product = Order.objects.get(pk=id).product
        order.user = request.user
        order.save()
        params['msg'] = f'ID:{id}を{order.qty}個カートに追加しました。'

    params['purchase_historys'] = Order.objects.filter(user=request.user, done=True)
    return render(request, 'ec_app/purchase_history.html', params)

def change_qty(request):
    # orderIDを取得する
    id = request.POST.get('id')
    qty = request.POST.get('qty')
    if qty.isdecimal() :
        order = Order.objects.get(pk=id)
        order.qty = qty
        if qty == 0:
            order.delete()
        else:
            order.save()
        return HttpResponse(status=204)

# 管理者ステータスのユーザーが利用できる商品登録
def admin_register_product(request):
    # 問 2-5-1 admin_register_product の pass を削除しましょう。
    pass
    # 問 2-5-2 params 変数に空の辞書を定義しましょう。

    # 問 2-5-3 POST の時の条件式を追加しましょう。

        # 問 2-5-3-1 form 変数に RegisterForm を格納しましょう。また、RegisterForm には request.POST と request.FILES をカンマ区切りで指定しましょう。

        # 問 2-5-3-2 form.is_valid の時の条件式を追加しましょう。

            # 問 2-5-3-3 True:True の時は、post 変数に form.save() を格納しましょう。また、引数には commit=False を指定しましょう。

            # 問 2-5-3-4 True:post.user にログインユーザーを格納しましょう。

            # 問 2-5-3-5 True:post をセーブしましょう。

            # 問 2-5-3-6 True:params 変数にキー：msg、バリュー：f'{post.product_name}の登録に成功しました。' を格納しましょう。


            # 問 2-5-3-7 False:False の時は、params 変数にキー：msg、バリュー：商品の登録に失敗しました。 を格納しましょう。

            # 問 2-5-3-8 False:params 変数にキー：form、バリュー：form を格納しましょう。

            # 問 2-5-3-9 False:render メソッドで admin_register_product.html を表示させましょう。また、params 辞書を HTML へ渡しましょう。

    # 問 2-5-4 params にキー：form、バリュー：RegisterForm を追加しましょう。

    # 問 2-5-5 render メソッドで admin_register_product.html を表示させましょう。また、params 辞書を HTML へ渡しましょう。


# 管理者ステータスのユーザーが利用できる商品一覧、削除、編集
def admin_product_list(request):
    # 問 3-3-1 admin_product_list 関数の pass を削除して、params 変数に空の辞書を定義しましょう。
    pass

    # 問 3-5-1 admin_product_list 関数の params 変数定義の下に、POST の際の条件式を追加しましょう。

        # 問 3-5-2 request.POST の中に btn_delete が含まれている時の条件式を追加しましょう。

            # 問 3-5-3 id 変数に request.POST.get('btn_delete') を格納しましょう。

            # 問 3-5-4 product 変数に Product テーブルから id 変数を利用して、選択されたレコードを get で取得しましょう。

            # 問 3-5-5 product 変数を削除しましょう。

        # 問 3-5-6 elif を使って request.POST の中に btn_delete が含まれている時の条件式を追加しましょう。

            # 問 3-5-7 id 変数に request.POST.get('btn_edit') を格納しましょう。

            # 問 3-5-8 product 変数に Product テーブルから id 変数を利用して、選択されたレコードを get で取得しましょう。

            # 問 3-5-9 edit_data 変数に getlist を使って編集データを格納しましょう。

            # 問 3-5-10 if 文を作成して、edit_data に変更なしのデータが保存されていたら、admin_product_list に redirect しましょう。getlist で取得したデータは、リスト型で格納されており、
            # １番目に商品名、２番目に価格が格納されています。



                # 問 3-5-11 else だった際に、product.product_name に edit_data[0] を格納しましょう。

                # 問 3-5-12 else:product.price に edit_data[1] を格納しましょう。

                # 問 3-5-13 else:product をセーブしましょう。

                # 問 3-5-14 else:params にキー：msg、バリュー：f'ID:{id}の変更に成功しました。' として格納しましょう。

    # 問 3-3-2 products 変数に Product テーブルのデータを格納しましょう。user がログインユーザーのもので絞りましょう。

    # 問 3-3-3 products 変数を id の順番に並べ替えましょう。

    # 問 3-3-5 admin_product_list 関数に戻り、products 変数に get_dict 関数の戻り値を格納しましょう。引数には products を渡しましょう。

    # 問 3-3-6 params にキー：products、バリュー：products を格納しましょう。

    # 問 3-3-7 render メソッドを使用して、admin_product_list.html を表示させましょう。引数には params 変数も渡しましょう。


# 商品検索
# 問 4-5-1 search_product 関数を編集しましょう。
def search_product(request):
    # 問 4-5-2 pass を削除して、params 変数に辞書を空で定義しましょう。
    pass

    # 問 4-5-3 POST の時の条件式を追加しましょう。

        # 問 4-5-3-1 category_id 変数に、request.POST.get('category') を格納しましょう。

        # 問 4-5-3-2 search_text 変数に、request.POST.get('search_text') を格納しましょう。

        # 問 4-5-3-3 products 変数に Product テーブルの全データを格納しましょう。

        # 問 4-5-3-4 もし、category_id に値が入っていれば、products 変数の category=category_id で filter をかけましょう。


        # 問 4-5-3-5 もし、search_text に値が入っていれば、Q オブジェクトを利用した filter を追加しましょう。


        # 問 4-5-3-7 products 変数に get_dict の返り値を格納しましょう。引数には products 変数を指定しましょう。

        # 問 4-5-3-8 params にキー：products、バリュー：products 変数を指定しましょう。

        # 問 4-5-3-9 ec_app/product_list.html を render しましょう。引数には params を渡しましょう。

    # 問 4-5-4 条件式の外で params にキー：form、バリュー：SearchProductForm を指定しましょう。また、SearchProductForm をインポートしましょう。

    # 問 4-5-5 ec_app/search_product.html を render しましょう。引数には params を渡しましょう。


# 辞書型を取得する関数
# 問 3-3-4 admin_product_list の外に、get_dict 関数を作成しましょう。引数には queryset を指定しましょう。

    # 問 3-3-4-1 products 変数に list(queryset.valuse()) を格納しましょう。

    # 問 3-3-4-2 choices 変数に Product.PRODUCT_CATEGORY を格納しましょう。

    # 問 3-3-4-3 choices 変数に dict((x, y) for x, y in choices) を再代入しましょう。

    # 問 3-3-4-4 for 文を追加して、products 変数を回しましょう。

        # 問 3-3-4-5 カテゴリーをキー：category、バリュー：それぞれの値を choices から取得して product に格納しましょう。

        # 問 3-3-4-6 画像の url を取得して、キー：img として格納しましょう。

    # 問 3-3-4-7 for 文の外で products 変数を return しましょう。
