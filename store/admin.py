from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *
 
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ProductCategories)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Session)
