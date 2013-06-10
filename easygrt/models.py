from django.db import models

# Create your models here.
# Decided to import all relevant GTFS data as seperate tables
# instead of writing script to consolidate data for flexibility

#See https://docs.djangoproject.com/en/dev/topics/db/models/
#See also https://docs.djangoproject.com/en/dev/ref/models/fields/
class Stops(models.Model):
    stop_id = models.IntegerField(primary_key = True, unique = True)
    stop_name = models.CharField(max_length = 50)
    stop_lat = models.DecimalField(max_digits = 8, decimal_places = 6)
    stop_lon = models.DecimalField(max_digits = 8, decimal_places = 6)
    
class StopTimes(models.Model):
    trip_id = models.IntegerField()
    arrival_time = models.CharField(max_length = 10)
    departure_time = models.CharField(max_length = 10)
    stop_id = models.IntegerField()

class Trips(models.Model):
    route_id = models.IntegerField()
    service_id = models.CharField(max_length = 7)
    trip_id = models.IntegerField(primary_key = True, unique = True)
    trip_headsign = models.CharField(max_length = 50)

class Routes(models.Model):
    route_id = models.IntegerField(primary_key = True, unique = True)
    route_long_name = models.CharField(max_length = 60)

class Calendar(models.Model):
    service_id = models.CharField(max_length = 5)
    monday = models.IntegerField()
    tuesday =  models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)

class CalendarDates(models.Model):
    service_id = models.CharField(max_length = 5)
    date = models.CharField(max_length = 10)
