from django.contrib import admin

from vitals.models import Vitals


# Register your models here.

@admin.register(Vitals)
class VitalsAdmin(admin.ModelAdmin):
    pass