from django.contrib import admin

from calls.models import Call


# Register your models here.

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    pass