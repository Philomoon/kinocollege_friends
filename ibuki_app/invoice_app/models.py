from django.db import models
from django.db.models import Sum, Count,F
from django.utils import timezone
from datetime import datetime,date,time
from datetime import datetime as dt
import datetime as dt_module

class Insurer(models.Model):
    insurer_name = models.CharField('保険者',max_length=6,default=1)
    
    def __str__(self) -> str:
        return self.insurer_name

class Client (models.Model):
    GENDER_CHOICES = (
        ('男性','男'),
        ('女性','女'),
    )

    # 名前
    client_name = models.CharField('利用者名',max_length=20)
    # ふりがな
    client_kana = models.CharField('ふりがな',max_length=100)
    # 性別
    client_gender = models.CharField('性別',max_length=2,choices=GENDER_CHOICES)
    # 電話番号
    number = models.CharField('電話番号',max_length=15)
    # 保険者
    insurer = models.ForeignKey(Insurer,on_delete=models.CASCADE)

    # 部屋番号
    room_number = models.CharField('部屋番号',max_length=10,null=True,blank=True)

    def __str__(self):
        return self.client_name
    

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    insurer = models.ForeignKey(Insurer,on_delete=models.CASCADE,default=1)
    base_price = models.DecimalField(max_digits=6,decimal_places=0)

class AddonType(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=6,decimal_places=0)

class Actual(models.Model):

    # 利用者名
    user_name = models.ForeignKey(Client,verbose_name='利用者名',on_delete=models.CASCADE)
    # 日付
    date = models.DateField('日付',default=timezone.now)
    # 日中一時
    dt_s = models.BooleanField('日中一時',default=False)
    # 開始時刻
    start_time = models.TimeField('開始時刻',default=dt_module.time(10,0))
    # 終了時刻
    end_time = models.TimeField('終了時刻',default=dt_module.time(15,0))
    #サービスタイプ
    type = models.ForeignKey(ServiceType,verbose_name='サービスタイプ',on_delete=models.CASCADE,null=True)
    # 入浴
    bathing = models.BooleanField('入浴',default=True)
    # 送迎
    transportation = models.BooleanField('送迎',default=True)
    # 食事
    meal = models.BooleanField('食事',default=True)
    # 備考
    notes = models.TextField('備考',blank=True)

    # 加算まとめ
    addons = models.ManyToManyField(AddonType)


    @property
    def duration(self):
        try:
            start_time = datetime.strptime(self.start_time, "%H:%M").time() if isinstance(self.start_time, str) else self.start_time
            end_time = datetime.strptime(self.end_time, "%H:%M").time() if isinstance(self.end_time, str) else self.end_time
        except ValueError:
            start_time = end_time = time()

        return (datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)).seconds / 3600

    def save(self, *args, **kwargs):

        # Overriding the save method to determine the service type based on duration
        if self.dt_s == True:
            if self.duration <= 3:  # For instance, this could be your criterion for short duration
                self.type = ServiceType.objects.get(name='日中一時支援(~4)')
            elif self.duration <= 6:
                self.type = ServiceType.objects.get(name='日中一時支援(4~8)')
            else:
                self.type = ServiceType.objects.get(name='日中一時支援(8~)')
        else:
            self.type = ServiceType.objects.get(name='生活介護')

        super().save(*args,**kwargs)

        if self.bathing:
            addon = AddonType.objects.get(name='入浴')
            self.addons.add(addon)
        if self.transportation:
            addon = AddonType.objects.get(name='送迎')
            self.addons.add(addon)
        if self.meal:
            addon = AddonType.objects.get(name='食事')
            self.addons.add(addon)

    @property
    def total_amount(self):
        base_amount = self.type.base_price
        addons_amount = sum([addon.base_price for addon in self.addons.all()])
        return base_amount + addons_amount


    class Meta:
        unique_together = ['user_name','date']

class Invoice(models.Model):
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    month = models.DateField()
    service_records = models.ManyToManyField(Actual)

    @property
    def total_amount(self):
        # Calculate the sum of all service totals for this invoice
        return self.serviceline_set.aggregate(total=Sum('total_amount'))['total']

class Service(models.Model):
    # Other fields...
    addons = models.ManyToManyField(AddonType)
    
    @property
    def total_amount(self):
        base_amount = self.type.base_price
        addons_amount = sum([addon.base_price for addon in self.addons.all()])
        return base_amount + addons_amount
    
class ServiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='serviceline_set')
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
    
    @property
    def total_amount(self):
        # Calculate the total amount for this service line
        return self.service.total_amount * self.count

