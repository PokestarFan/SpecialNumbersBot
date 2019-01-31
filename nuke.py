"""Nukes all current posts"""

from login import api

for i in api.GetUserTimeline(api.GetUser(screen_name='SpecialDateNum').id):
    api.DestroyStatus(i.id)