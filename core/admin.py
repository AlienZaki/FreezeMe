from django.contrib import admin
from .models import Client, Website, Requirement, Submission, Settings
from state.models import State

admin.site.site_header = 'Freeze-Me Administration'
admin.site.register(Client)
admin.site.register(Submission)
admin.site.register(Website)
admin.site.register(Requirement)
admin.site.register(Settings)
admin.site.register(State)