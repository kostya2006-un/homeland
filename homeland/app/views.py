from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView
from .models import Hotel, Apartament, Profile, Order, Status, Review, HotelRating
from .forms import CountryForm, PeopleNumberForm, DateForm, ReviewForm, HotelRatingForm
from django.utils import timezone
class IndexView(View):
    template_name = 'app/index.html'

    def get(self,request):
        # status_finished = Status.objects.get(status='завершенный')
        # status_in_procces = Status.objects.get(status='начатый')
        # today = timezone.now().date()
        #
        # for order in Order.objects.all():
        #     if order.leave_date < today:
        #         order.status = status_finished
        #     elif order.arrive_date <= today < order.leave_date:
        #         order.status = status_in_procces
        #     order.save()

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


class Hotel_Detail_View(View):
    template_name = 'app/hotel_detail.html'

    def get(self, request, *args, **kwargs):
        hotel = Hotel.objects.get(pk=kwargs['pk'])
        reviews = Review.objects.filter(hotel=hotel)
        form = ReviewForm()

        # Получаем оценку текущего пользователя для отеля (если она существует)
        user_rating = HotelRating.objects.filter(hotel=hotel, user=request.user).first()
        if user_rating:
            rating_form = HotelRatingForm(instance=user_rating)
        else:
            rating_form = HotelRatingForm()

        context = {
            'hotel': hotel,
            'reviews': reviews,
            'form': form,
            'rating_form': rating_form,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            hotel = Hotel.objects.get(pk=kwargs['pk'])
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotel_detail', pk=kwargs['pk'])

        rating_form = HotelRatingForm(request.POST)
        if rating_form.is_valid():
            hotel = Hotel.objects.get(pk=kwargs['pk'])
            rating = rating_form.save(commit=False)
            rating.hotel = hotel
            rating.user = request.user
            rating.save()
            return redirect('hotel_detail', pk=kwargs['pk'])

        hotel = Hotel.objects.get(pk=kwargs['pk'])
        reviews = Review.objects.filter(hotel=hotel)
        context = {
            'hotel': hotel,
            'reviews': reviews,
            'form': form,
            'rating_form': rating_form,
        }
        return render(request, self.template_name, context)

class ApartamentView(View):
    template_name = 'app/apartament_list.html'

    def get(self, request, pk):
        hotel = Hotel.objects.get(pk=pk)
        apartaments = Apartament.objects.filter(hotel=hotel)
        form = PeopleNumberForm()
        context = {
            'hotel':hotel,
            'form': form,
            'apartaments': apartaments,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = PeopleNumberForm(data=request.POST)
        if form.is_valid():
            hotel = Hotel.objects.get(pk=pk)
            number = form.cleaned_data['number']
            category = form.cleaned_data['category']
            res = Apartament.objects.filter(hotel=hotel)
            if number and category:
                res = Apartament.objects.filter(max_people=number, category=category, hotel=hotel)
            elif number:
                res = Apartament.objects.filter(max_people=number, hotel=hotel)
            elif category:
                res = Apartament.objects.filter(category=category, hotel=hotel)

            context = {
                'hotel': hotel,
                'form': form,
                'apartaments': res,
            }
            return render(request, self.template_name, context)

class Apartament_Detail_View(DetailView):
    template_name = 'app/apartament_detail.html'
    model = Apartament
    context_object_name = 'apartament'

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class IncrementBalance(View):
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        profile.money += 1000
        profile.save()

        return redirect('profile')

@method_decorator(login_required, name='dispatch')
class OrderView(View):
    template_name = 'app/order.html'

    def get(self, request, pk):
        form = DateForm()
        apartament = Apartament.objects.get(pk=pk)
        total_price = 0
        context = {
            'form': form,
            'apartament': apartament,
            'total_price': total_price
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = DateForm(data=request.POST)
        apartament = Apartament.objects.get(pk=pk)
        total_price = 0
        profile = Profile.objects.get(user=request.user)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            today = timezone.now().date()
            if start_date < today:
                messages.error(request, "Дата заезда не может быть раньше сегодняшней даты.")
            elif end_date <= start_date:
                messages.error(request, "Дата выезда должна быть позже даты заезда.")
            else:
                if 'calculate_order' in request.POST:
                    days = (end_date - start_date).days
                    total_price = apartament.price * days
                elif 'create_order' in request.POST:
                    days = (end_date - start_date).days
                    tot_price = apartament.price * days

                    if profile.money < tot_price:
                        messages.error(request, "Недостаточно средств")
                    else:
                        profile.money -= tot_price
                        profile.save()
                        Order.objects.create(
                            user=request.user,
                            apartament=apartament,
                            arrive_date=start_date,
                            leave_date=end_date,
                            total_amount=tot_price,
                            status=Status.objects.get_or_create(status="неначатый")[0]
                        )
                        return redirect('profile')

        context = {
            'form': form,
            'apartament': apartament,
            'total_price': total_price,
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
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


