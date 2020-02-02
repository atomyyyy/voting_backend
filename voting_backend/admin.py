from django.contrib import admin

from .models import VoteCampaign, VoteOption

admin.site.register(VoteCampaign)
admin.site.register(VoteOption)
