from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView,HotelListView,ApartamentView,ProfileView,IncrementBalance,OrderView,OrderDeleteView
urlpatterns = [
    path('',IndexView.as_view(),name = 'index'),
    path('hotels/',HotelListView.as_view(),name = 'hotels_list'),
    path('hotels/apartaments/<int:pk>/',ApartamentView.as_view(),name = 'apartaments'),
    path('profile/',ProfileView.as_view(),name = 'profile'),
    path('increment_balance',IncrementBalance.as_view(),name = 'increment_balance'),
    path('create_order/<int:pk>/',OrderView.as_view(),name = 'order'),
    path('order_delete/<int:pk>/',OrderDeleteView.as_view(),name = 'order_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)