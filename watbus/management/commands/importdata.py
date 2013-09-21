from django.core.management.base import BaseCommand, CommandError
import os.path
from sys import stdout
from datetime import time, date
from watbus.models import *
from django.db import transaction
import dse


#Allows for the easy importing of csv data.
#TODO: Switch to using csv model for parsing.
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

        #Necessary call to allow dse to work
        dse.patch_models()
        #Files must be loaded in particular order because of foreign key relationships.
        self._import_calendar(os.path.join(args[0], 'calendar.txt'))
        self._import_calendar_dates(os.path.join(args[0], 'calendar_dates.txt'))
        self._import_routes(os.path.join(args[0], 'routes.txt'))
        self._import_trips(os.path.join(args[0], 'trips.txt'))
        self._import_stops(os.path.join(args[0], 'stops.txt'))
        self._import_stop_times(os.path.join(args[0], 'stop_times.txt'))

        #Preform post-processing on database
        print "Performing post-processing"
        self._postprocess()

        print "Script completed."

    #Generator that parses each line of a given csv file (fpath).
    #Returns each row in hash with values mapped to column names in a dictionary.
    #Outputs the full path of each file being imported, as well as lines processed so far.
    def _parse_csv(self, fpath, separator):

        with open(fpath, 'r') as f:
            #First line should always be column names.
            #List comprehension strips whitespace characters from each header in the row.
            headers = [s.strip() for s in f.readline().split(',')]

            if not headers:
                raise CsvReadError(1, "Given file empty")
            
            #Keep a line count to output how many lines processed (for when getting impatient)
            curr_line = 1;

            #Iterate through each line in the file:
            for row in f:

                curr_line += 1

                #Carriage return (\r) prints output on same line in terminal.
                #TODO: Format this better
                stdout.write("\r{0} ..................... {1!s}".format(fpath, curr_line))
                stdout.flush()

                row_values = [s.strip("\n\t\"\'\r ") for s in row.split(separator)]

                if not row_values or len(row_values) != len(headers):
                    raise CsvReadError(curr_line, "Line not parsed correctly")

                #Create a dictionary that maps the first row (with header values) to the current row
                csv_dict = dict(zip(headers, row_values))
                #Freeze and return dictionary to calling function.
                yield csv_dict

            #Ensures that output written after all rows have been parsed is on a new line
            stdout.write("\n")


    #Converts YYYYMMDD format used in GTFS data to python date object.
    def _convert_date(self, datestr):
        return date(int(datestr[0:4]), int(datestr[4:6]), int(datestr[6:8]))

    #Converts the HH:MM:SS time format used in GTFS to python time object. 
    def _convert_time(self, timestr):

        #Time objects only accept hour values between 00..23, whereas GTFS uses the range 01..
        hour = int(timestr[0:2])
        if hour >= 24:
            hour -= 24

        return time(hour, int(timestr[3:5]), int(timestr[6:8]))

    def _import_calendar(self, path):

        with transaction.commit_on_success():
            with Calendar.delayed as d:
                for data in self._parse_csv(path, ','):
                    data['monday'] = int(data['monday'])
                    data['tuesday'] = int(data['tuesday'])
                    data['wednesday'] = int(data['wednesday'])
                    data['thursday'] = int(data['thursday'])
                    data['friday'] = int(data['friday'])
                    data['saturday'] = int(data['saturday'])
                    data['sunday'] = int(data['sunday'])
                    data['start_date'] = self._convert_date(data['start_date'])
                    data['end_date'] = self._convert_date(data['end_date'])
                    d.insert(data)

    def _import_calendar_dates(self, path):

        with transaction.commit_on_success():
            with CalendarDates.delayed as d:
                for data in self._parse_csv(path, ','):
                    data['date'] = self._convert_date(data['date'])
                    d.insert(data)


    def _import_routes(self, path):
        
        with transaction.commit_on_success():
            with Routes.delayed as d:
                for data in self._parse_csv(path, ','):
                    d.insert(data)

    def _import_trips(self, path):

        with transaction.commit_on_success():
            with Trips.delayed as d: 
                for data in self._parse_csv(path, ','):
                    d.insert(data)

    def _import_stops(self, path):

        with transaction.commit_on_success():
            with Stops.delayed as d:
                for data in self._parse_csv(path, ','):
                    data['stop_lat'] = float(data['stop_lat'])
                    data['stop_lon'] = float(data['stop_lon'])
                    data['parent_station_type'] = '' #DSE Will not accept none as a value

                    d.insert(data)

    def _import_stop_times(self, path):

        with transaction.commit_on_success():
            with StopTimes.delayed as d:
                for data in self._parse_csv(path, ','):
                        data['arrival_time'] = self._convert_time(data['arrival_time']).__str__()
                        data['departure_time'] = self._convert_time(data['departure_time']).__str__()
                        data['stop_sequence'] = int(data['stop_sequence'])
                        d.insert(data)

    def _postprocess(self):
        for stop in Stops.objects.filter(location_type=1) | Stops.objects.exclude(parent_station__exact=''):
            if (
                    (stop.parent_station == 'place_AST' or stop.stop_id == 'place_AST') or
                    (stop.parent_station == 'place_CBC' or stop.stop_id == 'place_CBC') or
                    (stop.parent_station == 'place_CST' or stop.stop_id == 'place_CST') or
                    (stop.parent_station == 'place_FGP' or stop.stop_id == 'place_FGP') or
                    (stop.parent_station == 'place_HHM' or stop.stop_id == 'place_HHM') or
                    (stop.parent_station == 'place_HIT' or stop.stop_id == 'place_HIT') 
                ):
                stop.parent_station_type = 0; #See models.py
            elif (
                    (stop.parent_station == 'place_BCI' or stop.stop_id == 'place_BCI') or
                    (stop.parent_station == 'place_CCD' or stop.stop_id == 'place_CCD') or
                    (stop.parent_station == 'place_ECI' or stop.stop_id == 'place_ECI') or
                    (stop.parent_station == 'place_HHS' or stop.stop_id == 'place_HHS') or
                    (stop.parent_station == 'place_KCI' or stop.stop_id == 'place_KCI') or
                    (stop.parent_station == 'place_PRHS' or stop.stop_id == 'place_PRHS') or
                    (stop.parent_station == 'place_SDS' or stop.stop_id == 'place_SDS') or
                    (stop.parent_station == 'place_SMH' or stop.stop_id == 'place_SMH') or
                    (stop.parent_station == 'place_STBS' or stop.stop_id == 'place_STBS') or
                    (stop.parent_station == 'place_WCI' or stop.stop_id == 'place_WCI') or
                    (stop.parent_station == 'place_WSS' or stop.stop_id == 'place_WSS')
                ):
                stop.parent_station_type = 1
            else:
                stop.parent_station_type = 2;

            stop.save()





