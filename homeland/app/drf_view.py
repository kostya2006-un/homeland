from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from app.models import Hotel,Country,Apartament,Review
from rest_framework.response import Response
from app.serializers import HotelListSerializer,HotelDetailSerializer,CountrySerializer,ApartamentSerializer,ApartamentDetailSerializer
from app.serializers import ReviewSerializer

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

class ApartamentApiView(APIView):
    def get(self,request,pk):
        hotel = Hotel.objects.get(pk=pk)
        apartaments = Apartament.objects.filter(hotel=hotel)
        serializer = ApartamentSerializer(apartaments,many=True)
        return Response(serializer.data)

class ApartamentDetailApiView(APIView):
    def get(self,request,pk):
        apartament = Apartament.objects.get(pk=pk)
        serializer = ApartamentDetailSerializer(apartament)
        return Response(serializer.data)

class ReviewApiView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



