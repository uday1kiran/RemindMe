from django.contrib import admin
from .models import Reminder
# Register your models here.

#to show read only fields like datecreated
class ReminderAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

#admin.site.register(Reminder)
admin.site.register(Reminder,ReminderAdmin)