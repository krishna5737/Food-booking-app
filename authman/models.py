from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
# Create your models here.
class City(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Hotels(models.Model):
    name=models.CharField(max_length=100)
    city=models.ForeignKey(to=City, on_delete=models.CASCADE)

    def tables_occupied_show(self):
        tables = Booking.objects.filter(hotel_name=self)
        return len(tables)

    def is_hotel_full(self):
        return self.tables_occupied_show() == 20
    def __str__(self):
        return self.name+" - "+str(self.city)+" - "+str(self.tables_occupied_show())

class Booking(models.Model):
    hotel_name = models.ForeignKey(to=Hotels,on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.hotel_name.name) + " - " + str(self.user) + " - "+str(self.time)