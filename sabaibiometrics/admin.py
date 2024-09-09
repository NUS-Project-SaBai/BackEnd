from django.contrib import admin

from clinicmodels.models import *

admin.site.register(Visit)
admin.site.register(Consult)
admin.site.register(Medication)
admin.site.register(Order)
admin.site.register(Patient)
admin.site.register(Vitals)