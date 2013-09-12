from django.contrib import admin
from watbus.models import Routes
from watbus.models import Calendar
from watbus.models import CalendarDates
from watbus.models import Trips
from watbus.models import Stops

# Register your models here.
admin.site.register(Routes)
admin.site.register(Calendar)
admin.site.register(CalendarDates)
admin.site.register(Trips)
admin.site.register(Stops)
