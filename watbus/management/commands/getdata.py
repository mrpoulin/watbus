from django.core.management.base import BaseCommand
import errno
import os, os.path
import urllib2
from StringIO import StringIO
from zipfile import ZipFile

class Command(BaseCommand):


    help = "Supply extraction path as only argument"
    
    def handle(self, *args, **options):
        
        CONTENT_URL = "http://www.regionofwaterloo.ca/opendatadownloads/GRT_GTFS.zip"

        if not args:
            print "No path supplied"
            return
        
        try:
            os.makedirs(args[0])
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        #Get GTFS zip from server
        response = urllib2.urlopen(CONTENT_URL)
        
        #Load zipfile into memory (StringIO) and extract to disk
        zipfile = ZipFile(StringIO(response.read()))
        zipfile.extractall(args[0])
