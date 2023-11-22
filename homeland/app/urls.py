from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView,HotelListView,ApartamentView
urlpatterns = [
    path('',IndexView.as_view(),name = 'index'),
    path('hotels/',HotelListView.as_view(),name = 'hotels_list'),
    path('hotels/apartaments/<int:pk>',ApartamentView.as_view(),name = 'apartaments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)