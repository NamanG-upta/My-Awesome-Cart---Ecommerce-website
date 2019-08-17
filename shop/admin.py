from django.contrib import admin
from .models import product, Contact, orders
from .models import ORDERSUPDATES
# Register your models here.

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(orders)
admin.site.register(ORDERSUPDATES)