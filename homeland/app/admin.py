from django.contrib import admin
from .models import Country,City,Hotel,Category,Apartament,NumberPeople
# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Category)
admin.site.register(Apartament)
admin.site.register(NumberPeople)