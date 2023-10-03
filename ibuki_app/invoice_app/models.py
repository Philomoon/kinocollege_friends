from django.db import models
from django.db.models import Sum, Count,F
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
from datetime import datetime,date,time
from datetime import datetime as dt
import datetime as dt_module

class Insurer(models.Model):
    insurer_name = models.CharField('保険者',max_length=6,default=1)
    
    def __str__(self) -> str:
        return self.insurer_name
class Class_OBST(models.Model):
    category = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.category
class Class_NUM(models.Model):
    category = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.category
    
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
    # 障害区分
    class_obst= models.ForeignKey(Class_OBST,on_delete=models.CASCADE)
    # 区分
    class_num= models.ForeignKey(Class_NUM,on_delete=models.CASCADE)
    # 保険者
    insurer = models.ForeignKey(Insurer,on_delete=models.CASCADE)


    def __str__(self):
        return self.client_name
    
#保険者毎の価格設定モデル
class ServiceType(models.Model):
    
    SERVICE_CHOICES = (
        ('A', '日中一時支援（〜４）'),
        ('B', '日中一時支援（４〜８）'),
        ('C', '日中一時支援（８〜）'),
        ('D','日中一時(併給）'),
        ('E','生活介護'),
    )
    servicename = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    insurers = models.ManyToManyField(Insurer, through='ServicePrice')

    def __str__(self):
        return self.get_servicename_display()

class ServicePrice(models.Model):
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    class_obst = models.ForeignKey(Class_OBST,on_delete=models.CASCADE)
    class_num = models.ForeignKey(Class_NUM,on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=6, decimal_places=0)

    @classmethod
    def get_price(cls,ins,serv,obst,num):
        try:
            obj = cls.objects.get(insurer=ins,service=serv,class_obst=obst,class_num=num)
            return obj.price
        except cls.DoesNotExist:
            return None

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['insurer', 'service', 'class_obst', 'class_num'], name='unique_fields_combination')
        ]

    def __str__(self):
        return f"{self.insurer}:{self.service}:{self.class_obst}:{self.class_num}:金額 {self.price}"




class AddonType(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=6,decimal_places=0)

    def __str__(self):
        return f"{self.name}:金額 {self.base_price}"

class Actual(models.Model):
    # 利用者名
    user_name = models.ForeignKey(Client,verbose_name='利用者名',on_delete=models.CASCADE)
    # 日付
    date = models.DateField('日付',default=timezone.now)
    # 生活介護・日中一時・併給
    DS_CHOICES = (
        ('日中一時','日中一時'),
        ('生活介護','生活介護'),
        ('併給','併給'),
    )
    ds = models.CharField('サービス種',max_length=30,choices=DS_CHOICES,default='日中一時')

    # 開始時刻
    start_time = models.TimeField('開始時刻',default=dt_module.time(10,0))
    # 終了時刻
    end_time = models.TimeField('終了時刻',default=dt_module.time(15,45))
    #サービスタイプ
    type = models.ForeignKey(ServiceType,verbose_name='サービスタイプ',on_delete=models.CASCADE,null=True)
    # 送迎（迎え）
    transportation1 = models.BooleanField('送迎（迎え）',default=True)
    # 送迎（送り）
    transportation2 = models.BooleanField('送迎（送り）',default=True)
    #送迎の回数
    trans_counts = models.IntegerField(
        validators=[
            MaxValueValidator(2),
            MinValueValidator(0),
        ],
        default=0
    )
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
        super(Actual,self).save(*args,**kwargs)

        # Overriding the save method to determine the service type based on duration
        self.trans_counts = self.transportation1 + self.transportation2
        
        self.addons.clear()
        if self.meal:
            addon = AddonType.objects.get(name='食事')
            self.addons.add(addon)
            
        if self.ds == '日中一時':
            if self.duration <= 3:  # For instance, this could be your criterion for short duration
                self.type = ServiceType.objects.get(id=4)
            elif self.duration <= 6:
                self.type = ServiceType.objects.get(id=5)
            else:
                self.type = ServiceType.objects.get(id=6)
        
        elif self.ds == '併給':
            self.type = ServiceType.objects.get(id=7)
        else:
            self.type = ServiceType.objects.get(id=8)

        super().save(*args,**kwargs)



    @property
    def total_amount(self):
        base_amount = ServicePrice.objects.get(insurer=self.user_name.insurer, service=self.type,class_obst=self.user_name.class_obst,class_num=self.user_name.class_num).price
        addons_amount =  sum([addon.base_price for addon in self.addons.all()])
        
        try:
            trans_addon = AddonType.objects.get(name="送迎")  # 送迎の正確な名称を使ってください
            trans_amount = trans_addon.base_price * self.trans_counts
        except AddonType.DoesNotExist:
            trans_amount = 0

        return base_amount + addons_amount + trans_amount


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

