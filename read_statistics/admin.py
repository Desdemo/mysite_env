from django.contrib import admin
from .models import ReadNum, ReadDeatil

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')


@admin.register(ReadDeatil)
class ReadDeatilAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')
