from django.contrib import admin
from .models import userInfo,userNotice

# Register your models here.
admin.site.register(userInfo)
admin.site.register(userNotice)