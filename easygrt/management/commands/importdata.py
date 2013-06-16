from django.core.management.base import BaseCommand, CommandError
import os.path
from sys import stdout
from time import time
from datetime import time, date
from easygrt.models import *


#Allows for the easy importing of csv data.
#TODO: Switch to using csv model for parsing.
#TODO: Speed up importing - it's too slow! See https://bitbucket.org/weholt/dse2 or BulkInsert (Django)
class Command(BaseCommand):

    class CsvReadError(Exception):
        def __init__(self, line, msg):
            self.line = line
            self.msg = msg

        def __str__(self):
            return "Error reading line {0!s}: {1}".format(self.line, self.msg)


    help = "Supply path to data files as only argument"
    

    #Method that is called when 'python manage.py importdata' is executed.
    def handle(self, *args, **options):
        
        if not args or not os.path.exists(args[0]) or not os.path.isdir(args[0]):
            print "Path supplied does not exist or is not a directory."
            return

        #Files must be loaded in particular order because of foreign key relationships.
        self._import_calendar(os.path.join(args[0], 'calendar.txt'))
        self._import_calendar_dates(os.path.join(args[0], 'calendar_dates.txt'))
        self._import_routes(os.path.join(args[0], 'routes.txt'))
        self._import_trips(os.path.join(args[0], 'trips.txt'))
        self._import_stops(os.path.join(args[0], 'stops.txt')),
        self._import_stop_times(os.path.join(args[0], 'stop_times.txt'))



    #Generator that parses each line of a given csv file (fname) and returns the line in a list.
    def _parse_csv(self, fpath, separator):
        with open(fpath, 'r') as f:
            headers = [s.strip() for s in f.readline().split(',')]

            if not headers:
                raise CsvReadError(1, "Given file empty")
            
            curr_line = 1;
            #Iterate through each line in the file:
            for row in f:

                curr_line += 1
                stdout.write("\r{0} ..................... {1!s}".format(fpath, curr_line))
                stdout.flush()

                columns = [s.strip() for s in row.split(separator)]

                if not columns or len(columns) != len(headers):
                    raise CsvReadError(curr_line, "Line not parsed correctly")

                csv_dict = dict(zip(headers, columns))
                yield csv_dict

            stdout.write("\n")


    def _convert_date(self, datestr):
        return date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:8]))

    def _convert_time(self, timestr):

        timestr = timestr.replace('24', '00')
        print timestr
        return time(int(timestr[0:2]), int(timestr[3:5]), int(timestr[6:8]))

    def _import_calendar(self, path):
        
        for data in self._parse_csv(path, ','):

            Calendar.objects.get_or_create(
                service_id = data['service_id'],
                monday = int(data['monday']),
                tuesday = int(data['tuesday']),
                wednesday = int(data['wednesday']),
                thursday = int(data['thursday']),
                friday = int(data['friday']),
                saturday = int(data['saturday']),
                sunday = int(data['sunday']),
                start_date = self._convert_date(data['start_date']),
                end_date = self._convert_date(data['end_date']),
                )

    def _import_calendar_dates(self, path):

        for data in self._parse_csv(path, ','):

            CalendarDates.objects.get_or_create(
                    service_id = Calendar.objects.get(service_id = data['service_id']),
                    date = self._convert_date(data['date']),
                    )


    def _import_routes(self, path):

        for data in self._parse_csv(path, ','):

            Routes.objects.get_or_create(
                    route_id = int(data['route_id']),
                    route_long_name = data['route_long_name'],
                    )

    def _import_trips(self, path):

        for data in self._parse_csv(path, ','):

            Trips.objects.get_or_create(
                    route_id = Routes.objects.get(route_id = int(data['route_id'])),
                    service_id = Calendar.objects.get(service_id = data['service_id']),
                    trip_id = int(data['trip_id']),
                    trip_headsign = data['trip_headsign'],
                    )

    def _import_stops(self, path):

        for data in self._parse_csv(path, ','):

            Stops.objects.get_or_create(
                    stop_id = int(data['stop_id']),
                    stop_name = data['stop_name'],
                    stop_lat = float(data['stop_lat']),
                    stop_lon = float(data['stop_lon']),
                    )

    def _import_stop_times(self, path):

        for data in self._parse_csv(path, ','):

            StopTimes.objects.get_or_create(
                    trip_id = Trips.objects.get(trip_id = int(data['trip_id'])),
                    arrival_time = self._convert_time(data['arrival_time']),
                    departure_time = self._convert_time(data['departure_time']),
                    stop_id = Stops.objects.get(stop_id = int(data['stop_id'])),
                    )

