from django.contrib import admin
from .models import Insurer,Class_OBST,Class_NUM,ServicePrice,ServiceType,AddonType
# Register your models here.


admin.site.register(Insurer)
admin.site.register(Class_OBST)
admin.site.register(Class_NUM)
admin.site.register(ServicePrice)
admin.site.register(ServiceType)
admin.site.register(AddonType)

