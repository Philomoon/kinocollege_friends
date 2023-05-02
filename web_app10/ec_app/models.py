from django.db import models
from django.contrib.auth import get_user_model

# 商品情報
class Product(models.Model):
    PRODUCT_CATEGORY = (
        ('1','食材'),
        ('2','家電'),
        ('3','調理器具'),
        ('4','書籍'),
        ('5','服'),
    )
    # 商品の名前
    product_name = models.CharField(max_length=100)
    # 商品の価格
    price = models.PositiveIntegerField()
    # 商品詳細
    product_detail = models.TextField()
    # 商品カテゴリー
    category = models.CharField(max_length=10,choices=PRODUCT_CATEGORY)
    # 商品画像
    img = models.ImageField(upload_to='images/')
    # 登録ユーザー
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    # 更新日
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name


# 注文情報
class Order(models.Model):
    # 注文者
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    # 注文商品
    product = models.ForeignKey(Product,models.CASCADE)
    # 数量
    qty = models.PositiveIntegerField(default=0)
    # その注文が決済済みかどうか 
    done = models.BooleanField(default=False)
    # 注文日
    ordered_at = models.DateField(null=True,blank=True)
    def __str__(self):
        return f'{self.user}の{self.product}を注文した履歴'
