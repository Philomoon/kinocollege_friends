from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory,inlineformset_factory
from django.urls import reverse_lazy,reverse
from django.utils import timezone
from .models import Client,Actual,Invoice,AddonType,ServicePrice
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
    fields = ['client_name','client_kana','client_gender','insurer','class_obst','class_num','insurance_id','max_amount']
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
    instance = get_object_or_404(Actual, id=actual_id)
    
    if request.method == "POST":
        form = ActualForm(request.POST, instance=instance)
        
        if form.is_valid():
            form.save()
            # リダイレクト先を設定（例：actual_listが詳細ページのURL名だと仮定）
            return redirect(reverse_lazy('actual_list'))
    
    else:
        form = ActualForm(instance=instance)

    return render(request, 'invoice_app/actual_edit.html', {'form': form})

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
    

    try:
        clients = Client.objects.get(id=name)
        service_priceA = ServicePrice.objects.get(
                        insurer=clients.insurer,
                        service=4,
                        class_obst=clients.class_obst,
                        class_num=clients.class_num,
                    ).price
        service_priceB = ServicePrice.objects.get(
                        insurer=clients.insurer,
                        service=5,
                        class_obst=clients.class_obst,
                        class_num=clients.class_num,
                    ).price
        service_priceC = ServicePrice.objects.get(
                        insurer=clients.insurer,
                        service=6,
                        class_obst=clients.class_obst,
                        class_num=clients.class_num,
                    ).price
        service_priceD = ServicePrice.objects.get(
                        insurer=clients.insurer,
                        service=7,
                        class_obst=clients.class_obst,
                        class_num=clients.class_num,
                    ).price   
    except (Client.DoesNotExist,ServicePrice.DoesNotExist):
        service_priceA = 1
        service_priceB = 1
        service_priceC = 1
        service_priceD = 940



    if name and year and month:
        service_records = Actual.objects.filter(user_name=name,date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    elif name:
        service_records = Actual.objects.filter(user_name=name).all().select_related('user_name','type').order_by('date')
    elif year and month:
        service_records = Actual.objects.filter(date__year=year,date__month=month).all().select_related('user_name','type').order_by('date')
    else:
        service_records = Actual.objects.all().select_related('user_name','type').order_by('date')
    
    
    total_sum = sum([record.total_amount for record in service_records])

    count_meal = service_records.filter(meal=True).count()
    amount_meal = count_meal * AddonType.objects.get(name='食事').base_price

    count_t1 = service_records.filter(transportation1=True).count()
    count_t2 = service_records.filter(transportation2=True).count()
    count_trans = count_t1 + count_t2
    amount_trans = count_trans * AddonType.objects.get(name='送迎').base_price
    
    count_serviceA = service_records.filter(type=4).count()
    count_serviceB = service_records.filter(type=5).count()
    count_serviceC = service_records.filter(type=6).count()
    count_serviceD = service_records.filter(type=7).count()

    amount_serviceA = count_serviceA * service_priceA
    amount_serviceB = count_serviceB * service_priceB
    amount_serviceC = count_serviceC * service_priceC
    amount_serviceD = count_serviceD * service_priceD

    
    params ={
        'service_records':service_records,
        'clients_list':clients_list,
        'client_name':name,
        'client_id':client_id,
        'year':year,
        'month':month,
        'name':name,
        'total_sum': total_sum,
        'count_meal':count_meal,
        'amount_meal':amount_meal,
        'count_trans':count_trans,
        'amount_trans':amount_trans,
        'count_serviceA':count_serviceA,
        'count_serviceB':count_serviceB,
        'count_serviceC':count_serviceC,
        'count_serviceD':count_serviceD,
        'amount_serviceA':amount_serviceA,
        'amount_serviceB':amount_serviceB,
        'amount_serviceC':amount_serviceC,
        'amount_serviceD':amount_serviceD,

        }
    
    return render(request,'invoice_app/service_records_list.html',params)

def record_list_modify(request):
    model = Actual
    fields = []
    template_name_suffix = '_modify_form' 

    success_url = reverse_lazy('client_list')


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

