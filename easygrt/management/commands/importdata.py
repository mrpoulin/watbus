from django.core.management.base import BaseCommand, CommandError
from django.core.management import callcommand

class Command(BaseCommand):


    help = "Supply path to data files as only argument"

    def handle(self, *args, **options):
        self.stdout.write("hello, world")

    


