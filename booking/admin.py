from django.contrib import admin
from .models import Category, Lawyer, Slot, Appointment

admin.site.register(Category)
admin.site.register(Lawyer)
admin.site.register(Slot)
admin.site.register(Appointment)
