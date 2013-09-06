from django.contrib import admin
from easygrt.models import Routes
from easygrt.models import Calendar
from easygrt.models import CalendarDates
from easygrt.models import Trips
from easygrt.models import Stops

# Register your models here.
admin.site.register(Routes)
admin.site.register(Calendar)
admin.site.register(CalendarDates)
admin.site.register(Trips)
admin.site.register(Stops)
