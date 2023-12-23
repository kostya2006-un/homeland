from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from app.models import Hotel,Country,Apartament,Review,Profile,Order
from rest_framework.response import Response
from app.serializers import HotelListSerializer,HotelDetailSerializer,CountrySerializer,ApartamentSerializer,ApartamentDetailSerializer
from app.serializers import ReviewSerializer,ProfileViewSerializer,AllOrdersSerializer,OrderSerializer,OrderDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser

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
    permission_classes = (IsAuthenticatedOrReadOnly, )

class ProfileViewApi(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileViewSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            profile.money += 1000
            profile.save()
            return Response({'message': 'Баланс успешно увеличен на 1000'}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Профиль не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllOrdersApiView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = AllOrdersSerializer
    permission_classes = (IsAdminUser,)

class OrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        apartament = serializer.validated_data['apartament']
        arrive_date = serializer.validated_data['arrive_date']
        leave_date = serializer.validated_data['leave_date']
        days = (leave_date - arrive_date).days
        total_price = apartament.price * days

        profile = self.request.user.profile
        if profile.money >= total_price:
            profile.money -= total_price
            profile.save()
            serializer.save(user=self.request.user,total_amount=total_price)
        else:
            raise ValidationError("Недостаточно средств для обработки заказа")

class OrderDetailApiView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_destroy(self, instance):
        profile = self.request.user.profile
        total_amount = instance.total_amount
        profile.money += total_amount
        profile.save()
        instance.delete()




