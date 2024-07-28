from django.contrib import admin

from pharmacies.models import Pharmacy


# Register your models here.
@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    pass