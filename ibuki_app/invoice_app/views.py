from django.shortcuts import render,redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
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
    clients = Client.objects.all().order_by('client_kana')
    params = {
        'clients':clients,
    }
    return render(request,'invoice_app/client_list.html',params)

class Client_modify(UpdateView):
    model = Client
    fields = ['client_name','client_kana','client_gender','number','insurer','room_number']
    template_name_suffix = '_modify_form' 

    success_url = reverse_lazy('client_list')

def Client_delete(request,client_id):
    if client_id:
        client_delete = Client.objects.get(id=client_id)
        client_delete.delete()
    return redirect('client_list')

def input(request):
    if request.method == 'POST':
        form = ActualForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input')
    else:
        form = ActualForm()
    params = {
        'form':form,
    }
    return render(request,'invoice_app/input.html',params)