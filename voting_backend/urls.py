from django.contrib import admin
from django.urls import path

from .views import CampaignOverviewListView, CampaignDetailRetrieveView, VoteRecordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('campaign/', CampaignOverviewListView.as_view()), # GET
    path('campaign/<int:campaign_id>/', CampaignDetailRetrieveView.as_view()), # GET
    path('vote/<int:campaign_id>/', VoteRecordView.as_view()) # POST
]
