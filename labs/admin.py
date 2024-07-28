from django.contrib import admin

from labs.models import Lab


# Register your models here.
@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    pass