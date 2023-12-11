from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView,HotelListView,ApartamentView,ProfileView,IncrementBalance,OrderView,OrderDeleteView,Hotel_Detail_View,Apartament_Detail_View
urlpatterns = [
    path('',IndexView.as_view(),name = 'index'),
    path('hotels/',HotelListView.as_view(),name = 'hotels_list'),
    path('hotel_detail/<int:pk>/',Hotel_Detail_View.as_view(),name = 'hotel_detail'),
    path('hotels/apartaments/<int:pk>/',ApartamentView.as_view(),name = 'apartaments'),
    path('apartament_detail/<int:pk>/',Apartament_Detail_View.as_view(),name = 'apartament_detail'),
    path('profile/',ProfileView.as_view(),name = 'profile'),
    path('increment_balance',IncrementBalance.as_view(),name = 'increment_balance'),
    path('create_order/<int:pk>/',OrderView.as_view(),name = 'order'),
    path('order_delete/<int:pk>/',OrderDeleteView.as_view(),name = 'order_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)