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
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_id = models.IntegerField()

class Trips(models.Model):
    route_id = models.IntegerField()
    service_id = models.CharField(max_length = 7)
    trip_id = models.IntegerField(primary_key = True, unique = True)
    trip_headsign = models.CharField(max_length = 50)

class Routes(models.Model):
    route_id = models.IntegerField(primary_key = True, unique = True)
    long_name = models.CharField(max_length = 60)

class Calendar(models.Model):
    service_id = models.CharField(max_length = 5)
    monday = models.IntegerField()
    tueday =  models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

class CalendarDates(models.Model):
    service_id = models.CharField(max_length = 5)
    date = models.DateField()
