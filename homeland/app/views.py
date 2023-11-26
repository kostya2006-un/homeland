from django.shortcuts import render
from django.views import View
from .models import Hotel,Apartament
from .forms import CountryForm,PeopleNumberForm
class IndexView(View):
    template_name = 'app/index.html'

    def get(self,request):
        return render(request,self.template_name)

class HotelListView(View):
    template_name = 'app/hotel_list.html'

    def get(self,request):
        form = CountryForm()
        context = {
            'hotels': Hotel.objects.all(),
            'form':form,
        }
        return render(request,self.template_name,context)

    def post(self,request):
        form = CountryForm(data=request.POST)

        if form.is_valid():
            country = form.cleaned_data['name']

            context = {
                'hotels':Hotel.objects.filter(country = country),
                'form':form,
            }
            return render(request,self.template_name,context)


class ApartamentView(View):

    template_name = 'app/apartament_list.html'
    def get(self,request,pk):
        hotel = Hotel.objects.get(pk = pk)
        apartaments = Apartament.objects.filter(hotel = hotel)
        form = PeopleNumberForm()
        context = {
            'form':form,
            'apartaments':apartaments,
        }
        return render(request,self.template_name,context)
    def post(self,request,pk):

        form = PeopleNumberForm(data = request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']

            context = {
                'form':form,
                'apartaments':Apartament.objects.filter(max_people = number,pk=pk),
            }
            return render(request,self.template_name,context)