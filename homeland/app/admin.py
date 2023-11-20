from django.contrib import admin
from .models import Country,City,Hotel,Category,HotelCategory,Apartament
# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Category)
admin.site.register(HotelCategory)
admin.site.register(Apartament)