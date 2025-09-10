from django.db import models
from django.contrib.auth.models import User

class TufModel(models.Model):
    name = models.CharField(max_length = 100)
    location =  models.CharField(max_length = 100)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.name
    

class BookingModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    turf = models.ForeignKey(TufModel, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.DecimalField(max_digits=6 , decimal_places=2)
    status = models.CharField(max_length=20 , default='Pending')


