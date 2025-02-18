from django.contrib import admin
from .models import Event

# admin.site.register(Event)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'max_attendees', 'start_date', 'create_date')
    ordering = ('-create_date',)
    search_fields = ('title', 'location')
    list_filter = ('location', 'category')

admin.site.register(Event, EventAdmin)
