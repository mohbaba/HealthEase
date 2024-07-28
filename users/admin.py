from django.contrib import admin

from users.models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    pass