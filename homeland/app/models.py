from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=20)

    def __str__(self):
        return self.country_name

class City(models.Model):
    city_name = models.CharField(max_length=20)

    def __str__(self):
        return self.city_name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=50)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    description = models.TextField()
    address = models.TextField()
    full = models.BooleanField(default=False)
    img = models.ImageField(upload_to='hotel_img',default='1.jpg')

    def __str__(self):
        return self.hotel_name

class Category(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class NumberPeople(models.Model):
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.number

class Apartament(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField()
    max_people = models.ForeignKey(NumberPeople,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='apartament_img',default='1.jpg')

    def __str__(self):
        return f'{self.name} | {self.hotel}'


