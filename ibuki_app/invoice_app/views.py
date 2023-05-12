from django.shortcuts import render,redirect
from .models import Client
from .forms import ClientForm,ActualForm

# サーバーからクライアントに返されるHTTPレスポンスを表すクラス
from django.http import HttpResponse
# 「request」という引数にはgetまたはpostの情報など）が渡される
def main(request):
    # render関数は、HTMLページを指定して、HTTPレスポンスとしてブラウザに返す
    # 1つ目の引数にrequestオブジェクト、2つ目の引数にテンプレート名
    return render(request, 'invoice_app/base.html')

def client_add(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')

    else:
        form = ClientForm()
    params = {
        'form':form,
    }
    return render(request, 'invoice_app/client_add.html',params)

def client_list(request):
    clients = Client.objects.all()
    params = {
        'clients':clients,
    }
    return render(request,'invoice_app/client_list.html',params)

def input(request):

    form = ActualForm()
    params = {
        'form':form,
    }
    return render(request,'invoice_app/input.html',params)