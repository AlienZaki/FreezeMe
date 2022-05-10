from django.contrib import admin
from .models import Client, Website, Requirement, Submission, Settings


admin.site.site_header = 'Freeze Me Administration'


class WebsiteAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'url',
        'created_at',
        'updated_at',
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'fname',
        'lname',
        'city',
        'state',
        'zip',
        'address_line1',
        'address_line2',
        'phone',
        'email',
        'ssn',
        'dob',
        'start_freeze_date',
        'end_freeze_date',
    ]


class RequirementAdmin(admin.ModelAdmin):
    list_display = [
        'website',
        'fname',
        'lname',
        'city',
        'state',
        'zip',
        'address_line1',
        'address_line2',
        'phone',
        'email',
        'ssn',
        'dob',
        'start_freeze_date',
        'end_freeze_date',
        'id_card',
        'passport',
        'driver_license',
        'residency'
    ]


class SettingsAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'value',
        ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Submission)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(Settings, SettingsAdmin)