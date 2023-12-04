from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from .models import Hotel,Apartament,Profile,Order,Status
from .forms import CountryForm,PeopleNumberForm,DateForm

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

class ProfileView(View):

    template_name = 'app/profile.html'

    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user)
        context = {
            'profile':profile,
            'orders':orders,
        }

        return render(request,self.template_name,context)

class IncrementBalance(View):
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        profile.money += 1000
        profile.save()

        return redirect('profile')

class OrderView(View):
    template_name = 'app/order.html'

    def get(self,request,pk):
        form = DateForm()
        apartament = Apartament.objects.get(pk=pk)
        context = {
            'form':form,
            'apartament':apartament,
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        form = DateForm(data=request.POST)
        apartament = Apartament.objects.get(pk=pk)
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            days = (end_date-start_date).days
            total_price = apartament.price * days
            if profile.money < total_price:
                messages.error(request, "Недостаточно средств")
            else:
                profile.money -= total_price
                profile.save()
                Order.objects.create(
                    user = request.user,
                    apartament = apartament,
                    arrive_date = start_date,
                    leave_date = end_date,
                    total_amount = total_price,
                    status=Status.objects.get_or_create(status="неначатый")[0]
                )

                return redirect('profile')
        context = {
            'form':form,
            'apartament': apartament,
        }
        return render(request,self.template_name,context)

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'app/order_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        order = self.get_object()
        total_amount = order.total_amount
        profile = order.user.profile

        # Возврат денег пользователю
        profile.money += total_amount
        profile.save()

        return super().form_valid(form)