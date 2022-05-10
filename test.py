import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FreezeMe.settings")
django.setup()

from state.models import State
states = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

with open('test', 'r') as f:
    for s in f.readlines():
        if s.strip('\n') not in states:
            State.objects.create(
                abbreviation=s.strip('\n')
            )