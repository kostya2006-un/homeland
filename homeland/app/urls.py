from django.urls import path
from .views import IndexView,HotelListView
urlpatterns = [
    path('',IndexView.as_view(),name = 'index'),
    path('hotels/',HotelListView.as_view(),name = 'hotels_list')
]