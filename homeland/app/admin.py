from django.contrib import admin
from .models import Country,City,Hotel,Category,Apartament,NumberPeople,Order,Status,Review

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Category)
admin.site.register(Apartament)
admin.site.register(NumberPeople)
admin.site.register(Order)
admin.site.register(Status)
admin.site.register(Review)