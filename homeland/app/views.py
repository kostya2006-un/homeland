from django.shortcuts import render
from django.views import View
from .models import Hotel
class IndexView(View):
    template_name = 'app/index.html'

    def get(self,request):
        return render(request,self.template_name)

class HotelListView(View):
    template_name = 'app/hotel_list.html'

    def get(self,request):
        context = {
            'hotels': Hotel.objects.all(),
        }
        return render(request,self.template_name,context)