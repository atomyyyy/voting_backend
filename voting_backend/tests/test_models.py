import datetime
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError
import voting_backend.models as models


class TestVoteCampaignModel(TestCase):
    model = models.VoteCampaign

    def setUp(self):
        self.campaign = self.model.objects.create(
            campaign_id=1,
            question='How are you',
            start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
            end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)
        )
    
    def test_string_representation(self):
        self.assertEqual(str(self.campaign), '1: How are you')
    
    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 2, 1, 0, 0, 0))
    def test_can_identify_inactive_status(self, mock_datetime):
        self.assertEqual(self.campaign.is_active_campaign, False)
    
    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_identify_active_status(self, mock_datetime):
        self.assertEqual(self.campaign.is_active_campaign, True)
    
    def test_can_prevent_saving_record_with_improper_start_end_date(self):
        with self.assertRaises(ValidationError):
            self.campaign = self.model.objects.create(
                question='How are you',
                start_time=datetime.datetime(2000, 2, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 1, 1, 0, 0, 0)
            )
