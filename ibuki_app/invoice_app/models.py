from django.db import models

# Create your models here.
class Client (models.Model):
    GENDER_CHOICES = (
        ('男性','男'),
        ('女性','女'),
    )

    # 名前
    client_name = models.CharField(max_length=20)
    # ふりがな
    client_kana = models.CharField(max_length=100)
    # 性別
    client_gender = models.CharField(max_length=2,choices=GENDER_CHOICES)
    # 電話番号
    number = models.CharField(max_length=15)
    # 保険者
    insurer = models.CharField(max_length=10)
    # 部屋番号
    room_number = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.client_name

class Actual(models.Model):

    # 利用者名
    user_name = models.ForeignKey(Client,on_delete=models.CASCADE)
    # 日付
    date = models.DateField()
    # 開始時刻
    start_time = models.TimeField()
    # 終了時刻
    end_time = models.TimeField()
    # 入浴
    bathing = models.BooleanField(default=True)
    # 送迎
    transportation = models.BooleanField(default=True)
    # 食事
    meal = models.BooleanField(default=True)
    # 備考
    notes = models.TextField(blank=True)