from django.db import models
import datetime
# Create your models here.
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
    insurer = models.CharField('保険者',max_length=10)
    # 部屋番号
    room_number = models.CharField('部屋番号',max_length=10,null=True,blank=True)

    def __str__(self):
        return self.client_name

class Actual(models.Model):

    # 利用者名
    user_name = models.ForeignKey(Client,verbose_name='利用者名',on_delete=models.CASCADE)
    # 日付
    date = models.DateField('日付')
    # 開始時刻
    start_time = models.TimeField('開始時刻',default=datetime.time(10,0))
    # 終了時刻
    end_time = models.TimeField('終了時刻',default=datetime.time(15,0))
    # 入浴
    bathing = models.BooleanField('入浴',default=True)
    # 送迎
    transportation = models.BooleanField('送迎',default=True)
    # 食事
    meal = models.BooleanField('食事',default=True)
    # 備考
    notes = models.TextField('備考',blank=True)

    class Meta:
        unique_together = ['user_name','date']
