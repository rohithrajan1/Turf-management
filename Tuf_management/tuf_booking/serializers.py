from rest_framework import serializers
from datetime import datetime, date
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username' , 'email' , 'password']

class TufSerializer(serializers.ModelSerializer):
    class Meta:
        model = TufModel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = BookingModel
        fields = ['id', 'username', 'turf', 'date', 'start_time', 'end_time', 'total_price', 'status']
        read_only_fields = ['username', 'total_price', 'status'] 

    def validate(self, data):
        turf = data['turf']
        start = data['start_time']
        end = data['end_time']
        date = data['date']
       

        existing_bookings = BookingModel.objects.filter(date=date)

        for booking in existing_bookings:
            existing_start = booking.start_time
            existing_end = booking.end_time
            existing_turf = booking.turf

            if (start < existing_end and end > existing_start and turf == existing_turf):
                raise serializers.ValidationError("This time slot is already booked.")
    
        if end <= start:
            raise serializers.ValidationError("End time must be after start time")
        return data


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user  
        turf = validated_data['turf']
        start = validated_data['start_time']
        end = validated_data['end_time']

        duration = (datetime.combine(date.min, end) - datetime.combine(date.min, start)).seconds / 3600
        total_price = duration * float(turf.price_per_hour)

        return BookingModel.objects.create(
            user=user,
            turf=turf,
            date=validated_data['date'],
            start_time=start,
            end_time=end,
            total_price=total_price,
            status='Pending'
        )