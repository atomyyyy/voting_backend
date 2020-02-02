from django.contrib import admin
from django.urls import path

from .views import (CampaignDetailRetrieveView, CampaignOverviewListView,
                    VoteRecordView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('campaign/', CampaignOverviewListView.as_view(), name='campaign_list'), # GET
    path('campaign/<int:campaign_id>/', CampaignDetailRetrieveView.as_view(), name='campaign_detail'), # GET
    path('vote/<int:campaign_id>/', VoteRecordView.as_view(), name='vote') # POST
]
