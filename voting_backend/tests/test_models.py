import datetime
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

import voting_backend.models as models


class TestVoteCampaignModel(TestCase):
    multi_db = True
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
    def test_can_identify_closed_status(self, mock_datetime):
        self.assertEqual(self.campaign.status, 'CLOSED')
    
    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_identify_active_status(self, mock_datetime):
        self.assertEqual(self.campaign.status, 'ACTIVE')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(1999, 1, 1, 0, 0, 0))
    def test_can_identify_not_start_status(self, mock_datetime):
        self.assertEqual(self.campaign.status, 'NOT_START')
    
    def test_can_prevent_saving_record_with_improper_start_end_date(self):
        with self.assertRaises(ValidationError):
            self.campaign = self.model.objects.create(
                question='How are you',
                start_time=datetime.datetime(2000, 2, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 1, 1, 0, 0, 0)
            )


class TestVoteOptionModel(TestCase):
    multi_db = True
    model = models.VoteOption

    def setUp(self):
        campaign = models.VoteCampaign.objects.create(
            question='How are you',
            start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
            end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)
        )
        self.option = self.model.objects.create(
            campaign=campaign,
            option_code='1',
            option_detail='I am fine'
        )
    
    def test_string_representation(self):
        self.assertEqual(str(self.option), '1: I am fine')


class TestVoteRecordModel(TestCase):
    multi_db = True
    model = models.VoteRecord
    user_id = 'A123456'

    def setUp(self):
        self.campaign = models.VoteCampaign.objects.create(
            question='How are you',
            start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
            end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)
        )
        self.first_option = models.VoteOption.objects.create(
            campaign=self.campaign,
            option_code='1',
            option_detail='I am fine'
        )
        self.second_option = models.VoteOption.objects.create(
            campaign=self.campaign,
            option_code='2',
            option_detail='I am not fine'
        )
        self.record = self.model.objects.create(
            user_id=self.user_id,
            option=self.first_option,
            campaign=self.campaign
        )
    
    def test_can_prevent_inserting_two_vote_record_from_same_persion(self):
        with self.assertRaises(IntegrityError):
            self.model.objects.create(
                user_id=self.user_id,
                option=self.second_option,
                campaign=self.campaign
            )
