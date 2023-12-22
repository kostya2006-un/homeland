from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView,HotelListView,ApartamentView,ProfileView,IncrementBalance,OrderView,OrderDeleteView,Hotel_Detail_View,Apartament_Detail_View
from app.drf_view import HotelApiView,HotelDetailApiView,CountryApiView,ApartamentApiView,ApartamentDetailApiView,ReviewApiView
from app.drf_view import ProfileViewApi,OrderApiView
urlpatterns = [
    path('',IndexView.as_view(),name = 'index'),
    path('hotels/',HotelListView.as_view(),name = 'hotels_list'),
    path('hotel_detail/<int:pk>/',Hotel_Detail_View.as_view(),name = 'hotel_detail'),
    path('hotels/apartaments/<int:pk>/',ApartamentView.as_view(),name = 'apartaments'),
    path('apartament_detail/<int:pk>/',Apartament_Detail_View.as_view(),name = 'apartament_detail'),
    path('profile/',ProfileView.as_view(),name = 'profile'),
    path('increment_balance',IncrementBalance.as_view(),name = 'increment_balance'),
    path('create_order/<int:pk>/',OrderView.as_view(),name = 'order'),
    path('order_delete/<int:pk>/',OrderDeleteView.as_view(),name = 'order_delete'),
    #----------- API ----------------
    path('api/v1/hotellist/',HotelApiView.as_view()),
    path('api/v1/hotellist/<int:pk>/',HotelDetailApiView.as_view()),
    path('api/v1/countries',CountryApiView.as_view()),
    path('api/v1/apartaments/<int:pk>/',ApartamentApiView.as_view()),
    path('api/v1/apartament_detail/<int:pk>/',ApartamentDetailApiView.as_view()),
    path('api/v1/reviews/',ReviewApiView.as_view()),
    path('api/v1/profile/',ProfileViewApi.as_view()),
    path('api/v1/orders/',OrderApiView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)