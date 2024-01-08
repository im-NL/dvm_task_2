from django.db import models
from django.conf import settings

# Create your models here.

class Train(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    departure_time = models.TimeField()
    duration = models.IntegerField()
    gen_price= models.IntegerField()
    days = models.CharField(max_length=21) # Mon, Tue, Wed, Thu, Fri, Sat, Sun

    def __str__(self):
        return self.name

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.CharField(max_length=100)
    arrival = models.TimeField()
    departure = models.TimeField()
    day = models.IntegerField()

    def __str__(self):
        return self.station

class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    seat_no = models.IntegerField()
    date = models.DateField(auto_now=True)

class Seats(models.Model):
    classes = {
        ('GEN', 'General'),
        ('SL', 'Sleeper'),
        ('3A', '3rd AC'),
        ('2A', '2nd AC'),
        ('1A', '1st AC'),
    }
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    total_seats = models.IntegerField()
    seats_booked = models.IntegerField(default=0)
    seat_class = models.CharField(max_length=3, choices=classes)