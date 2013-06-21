from django.db import models

# Create your models here.
# Decided to import all relevant GTFS data as seperate tables
# instead of writing script to consolidate data for flexibility

#See https://docs.djangoproject.com/en/dev/topics/db/models/
#See also https://docs.djangoproject.com/en/dev/ref/models/fields/
class Calendar(models.Model):
    service_id = models.CharField(primary_key = True, max_length = 5)
    monday = models.BooleanField()
    tuesday =  models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

class CalendarDates(models.Model):
    #db_column set since django automatically appends _id to foregin keys. I.e. django
    #would name this column 'service_id_id'
    service_id = models.ForeignKey(Calendar, db_column='service_id')
    date = models.DateField()
    
class Routes(models.Model):
    route_id = models.IntegerField(primary_key = True, unique = True)
    route_long_name = models.CharField(max_length = 60)

class Trips(models.Model):
    route_id = models.ForeignKey(Routes, db_column='route_id')
    service_id = models.ForeignKey(Calendar, db_column='service_id')
    trip_id = models.IntegerField(primary_key = True, unique = True)
    trip_headsign = models.CharField(max_length = 50)

class Stops(models.Model):
    stop_id = models.IntegerField(primary_key = True, unique = True)
    stop_name = models.CharField(max_length = 50)
    stop_lat = models.DecimalField(max_digits = 8, decimal_places = 6)
    stop_lon = models.DecimalField(max_digits = 8, decimal_places = 6)
    
class StopTimes(models.Model):
    trip_id = models.ForeignKey(Trips, db_column='trip_id')
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_id = models.ForeignKey(Stops, db_column='stop_id')


