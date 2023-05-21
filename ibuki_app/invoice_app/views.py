from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Client,Actual
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


def actual_list(request):
    actuals = Actual.objects.all().order_by('date')
    params = {
        'actuals':actuals,
    }
    return render(request,'invoice_app/actual_list.html',params)

def actual_edit(request, actual_id):
    actual = get_object_or_404(Actual, id=actual_id)  # 指定されたIDのActualデータを取得
    if request.method == 'POST':
        form = ActualForm(request.POST, instance=actual)
        if form.is_valid():
            form.save()  # フォームの内容を保存
            return redirect('actual_list')  # 一覧ページにリダイレクト
    else:
        form = ActualForm(instance=actual)
    return render(request, 'invoice_app/actual_edit.html', {'form': form, 'actual': actual})

def actual_edit_ajax(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    value = request.POST.get('value')

    actual = get_object_or_404(Actual, id=id)  # 指定されたIDのActualデータを取得

    if request.method == 'POST':
        form = ActualForm(request.POST, instance=actual)
        if form.is_valid():
            form.save()  # フォームの内容を保存
            return redirect('actual_list')  # 一覧ページにリダイレクト

def actual_delete(request,actual_id):
    if actual_id:
        actual_delete = Actual.objects.get(id=actual_id)
        actual_delete.delete()
    return redirect('actual_list')

def actual_bulk_edit(request):
    queryset = Actual.objects.all()

    ActualFormSet = modelformset_factory(Actual, form=ActualForm, extra=0)
    formset = ActualFormSet(request.POST or None, queryset = queryset)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect('actual_list')
    
    params = {
        'actuals':formset,
        'msg':"更新しました",
    }
    return render(request,'invoice_app/actual_list.html',params)

