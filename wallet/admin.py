from django.contrib import admin

from wallet.models import Wallet, Transaction


# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass