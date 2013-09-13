from django.db import models

# Create your models here.
# Decided to import all relevant GTFS data as seperate tables
# instead of writing script to consolidate data for flexibility

#See https://docs.djangoproject.com/en/dev/topics/db/models/
#See also https://docs.djangoproject.com/en/dev/ref/models/fields/
class Calendar(models.Model):
    service_id = models.CharField(primary_key = True, max_length = 60)
    monday = models.BooleanField()
    tuesday =  models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "{0}:{1}->{2}".format(self.service_id, self.start_date, self.end_date)

class CalendarDates(models.Model):
    #db_column set since django automatically appends _id to foregin keys. I.e. django
    #would name this column 'service_id_id'
    service_id = models.ForeignKey(Calendar, db_column='service_id')
    date = models.DateField()

    def __unicode__(self):
        return "{0}:{1}".format(self.service_id, self.date)
    
class Routes(models.Model):
    route_id = models.CharField(primary_key = True, unique = True, max_length = 60)
    route_long_name = models.CharField(max_length = 60)

    def __unicode__(self):
        return "{0}:{1}".format(self.route_id, self.route_long_name)

class Trips(models.Model):
    route_id = models.ForeignKey(Routes, db_column='route_id')
    service_id = models.ForeignKey(Calendar, db_column='service_id')
    trip_id = models.CharField(primary_key = True, unique = True, max_length = 60)
    trip_headsign = models.CharField(max_length = 50)

    def __unicode__(self):
        return "{0}:{1}".format(self.trip_id, self.trip_headsign)

class Stops(models.Model):
    stop_id = models.CharField(primary_key = True, unique = True, max_length = 30)
    stop_name = models.CharField(max_length = 50)
    stop_lat = models.DecimalField(max_digits = 8, decimal_places = 6)
    stop_lon = models.DecimalField(max_digits = 8, decimal_places = 6)
    location_type = models.BooleanField()
    parent_station = models.CharField(max_length = 15)

    def __unicode__(self):
        return "{0}:{1} PART OF {2}".format(self.stop_id, self.stop_name, self.parent_station)
    
class StopTimes(models.Model):
    trip_id = models.ForeignKey(Trips, db_column='trip_id')
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_id = models.ForeignKey(Stops, db_column='stop_id')
    stop_sequence = models.IntegerField()

    def __unicode__(self):
        return "Trip:{0},Stop:{1}:{2}->{3},{4}".format(self.trip_id, self.stop_id, self.arrival_time, self.departure_time, self.stop_sequence)
