from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory,inlineformset_factory
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Client,Actual,Invoice,ServiceLine,Service
from .forms import ClientForm,ActualForm,InvoiceCreateForm
from django.views import generic
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import datetime
from datetime import timedelta,date
from django.http import HttpResponse


def main(request):
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
    return render(request, 'invoice_app/main.html',params)

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
            actual = form.save(commit=False)
            actual.save()

            form.save_m2m()

            return redirect('input')
    else:
        form = ActualForm()
    params = {
        'form':form,
    }
    return render(request,'invoice_app/input.html',params)


def actual_list(request):
    actuals = Actual.objects.all()
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

def actual_bulk_edit(request):
    if request.method == "POST":
        records_to_update = {}
        # Get all records and set checkboxes to off
        all_records = Actual.objects.all()
        for record in all_records:
            record.dts = False
            record.transportation1 = False
            record.transportation2 = False
            record.meal = False
            record.addons.clear()
            record.save()
            records_to_update[record.id] = record

        for key, value in request.POST.items():
            if key.startswith("start_time-") or key.startswith("end_time-") or key.startswith("dt_s") or key.startswith("transportation-") or key.startswith("bathing-") or key.startswith("meal-") or key.startswith("notes-"):
                id = key.split('-')[1]
                record = records_to_update.get(id)
                if not record:
                    record = Actual.objects.get(id=id)
                    records_to_update[id] = record

                if key.startswith("start_time-"):
                    record.start_time = value
                elif key.startswith("end_time-"):
                    record.end_time = value
                elif key.startswith("ds-"):
                    record.dt_s = (value == 'on')
                elif key.startswith("transportation1-"):
                    record.transportation1 = (value == 'on')
                elif key.startswith("transportation2-"):
                    record.transportation2 = (value == 'on')
                elif key.startswith("meal-"):
                    record.meal = (value == 'on')
                elif key.startswith("notes-"):
                    record.notes = value
        
        for record in records_to_update.values():
            record.save()
    
    return redirect('record_list_modify')


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


def service_record_list(request):

    clients_list = Client.objects.all()
    today = date.today()

    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')
        name = request.POST.get('name')
        client_id = request.POST.get('name')
    else:
        year = today.year
        month = today.month
        name = None
        client_id = None
    
    
    if name and year and month:
        service_records = Actual.objects.filter(user_name=name,date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    elif name:
        service_records = Actual.objects.filter(user_name=name).all().select_related('user_name','type').order_by('date')
    elif year and month:
        service_records = Actual.objects.filter(date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    else:
        service_records = Actual.objects.all().select_related('user_name','type').order_by('date')
    
    

    params ={
        'service_records':service_records,
        'clients_list':clients_list,
        'client_name':name,
        'client_id':client_id,
        'year':year,
        'month':month,
        'name':name,

        }
    return render(request,'invoice_app/service_records_list.html',params)

def record_list_modify(request):

    clients_list = Client.objects.all()

    year = request.POST.get('year')
    month = request.POST.get('month')
    name = request.POST.get('name')
    
    if name and year and month:
        service_records = Actual.objects.filter(user_name=name,date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    elif name:
        service_records = Actual.objects.filter(user_name=name).all().select_related('user_name','type').order_by('date')
    elif year and month:
        service_records = Actual.objects.filter(date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    else:
        service_records = Actual.objects.all().select_related('user_name','type').order_by('date')

    

    params ={
        'service_records':service_records,
        'clients_list':clients_list,
    }
    return render(request,'invoice_app/records_modify.html',params)


def custmer_view(request,client_id):
    InvoiceFormSet = inlineformset_factory(
        Client,
        Actual,
        fields=('user_name','type'),
        extra=1,
    )    
    
    client = get_object_or_404(Client,id=client_id)

    if request.method == 'POST':
        formset = InvoiceFormSet(request.POST,instance=client)
        if formset.is_valid():
            formset.save()
            return redirect('custmer_view',user_id=client.id)
    else:
        formset = InvoiceFormSet(isinstance=client)

    return render(request,'customer.html',{'formset':formset})

def view_invoices_for_month(request, year, month):
    # 入力された年と月に基づいて開始日と終了日を取得します。
    start_date = timezone.datetime(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)

    # 指定された期間中に作成された請求書を取得します。
    invoices = Invoice.objects.filter(created_at__range=(start_date, end_date))

    return render(request, 'invoices.html', {'invoices': invoices})

