from rest_framework.views import APIView
from app.models import Hotel,Country
from rest_framework.response import Response
from app.serializers import HotelListSerializer,HotelDetailSerializer,CountrySerializer

class HotelApiView(APIView):
    def get(self,request):
        hotels = Hotel.objects.all()
        serializer = HotelListSerializer(hotels,many=True)
        return Response(serializer.data)

class HotelDetailApiView(APIView):

    def get(self,request, pk):
        hotel = Hotel.objects.get(pk=pk)
        serializer = HotelDetailSerializer(hotel)
        return Response(serializer.data)

class CountryApiView(APIView):

    def get(self,request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries,many=True)
        return Response(serializer.data)