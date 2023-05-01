from django.shortcuts import render

# サーバーからクライアントに返されるHTTPレスポンスを表すクラス
from django.http import HttpResponse
# 「request」という引数にはgetまたはpostの情報など）が渡される
def main(request):
    # render関数は、HTMLページを指定して、HTTPレスポンスとしてブラウザに返す
    # 1つ目の引数にrequestオブジェクト、2つ目の引数にテンプレート名
    return render(request, 'invoice/main.html')

def client_add(request):

    return render(request, 'invoice/client_add.html')


def input(request):

    return render(request,'invoice/input.html')