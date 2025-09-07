from django.contrib import admin
from .models import Sensors, Devices, DevicesView

# python manage.py createsuperuser
# python manage.py changepassword
# python manage.py runserver
#
# python manage.py showmigrations

# Register your models here.
admin.site.register(Sensors)
admin.site.register(Devices)
admin.site.register(DevicesView)