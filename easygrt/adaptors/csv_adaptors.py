from adaptor.model import CsvModel, CsvDbModel
from adaptor.fields import *
from easygrt.models import *
from datetime import datetime

def transform_date(date):
        return datetime(int(date[:4]),int(date[4:6]),int(date[6:])).date().__str__()

class CalendarAdaptor(CsvModel):

    service_id = CharField()
    monday = IntegerField()
    tuesday =  IntegerField()
    wednesday = IntegerField()
    thursday = IntegerField()
    friday = IntegerField()
    saturday = IntegerField()
    sunday = IntegerField()
    start_date = CharField(prepare=transform_date)
    end_date = CharField(prepare=transform_date)

    class Meta:
        dbModel = Calendar
        has_header = True
        delimiter = ','


class CalendarDatesAdaptor(CsvModel):
    
    service_id = CharField()
    date = CharField(prepare=transform_date)
    exception_type = IgnoredField()

    class Meta:
        dbModel = CalendarDates
        has_header = True
        delimiter = ','

class RoutesAdaptor(CsvModel):

    route_id = IntegerField()
    route_short_name = IgnoredField()
    route_long_name = CharField()
    route_type = IgnoredField()

    class Meta:
        dbModel = Routes
        has_header = True
        delimiter = ','

class StopTimesAdaptor(CsvModel):

    trip_id = IntegerField()
    arrival_time = CharField()
    departure_time = CharField()
    stop_id = IntegerField()
    stop_sequence = IgnoredField()

    class Meta:
        dbModel = StopTimes
        has_header = True
        delimiter = ','

class StopsAdaptor(CsvModel):

    stop_id = IntegerField()
    stop_name = CharField()
    stop_lat = DecimalField()
    stop_lon = DecimalField()
    stop_desc = IgnoredField()

    class Meta:
        dbModel = Stops
        has_header = True
        delimiter = ','


class TripsAdaptor(CsvModel):

    route_id = IntegerField()
    service_id = CharField()
    trip_id = IntegerField()
    trip_headsign = CharField()
    block_id = IgnoredField()
    shape_id = IgnoredField()

    class Meta:
        dbModel = Trips
        has_header = True
        delimiter = ','
