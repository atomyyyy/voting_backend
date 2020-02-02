import datetime
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from voting_backend import models


class TestCampaignOverviewListView(APITestCase):
    multi_db = True

    def setUp(self):
        self.campaigns = models.VoteCampaign.objects.bulk_create([
            models.VoteCampaign(
                question='How are you',
                start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)                
            ),
            models.VoteCampaign(
                question='How old are you',
                start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)                
            ),
        ])

        self.option = models.VoteOption.objects.create(
            campaign=models.VoteCampaign.objects.get(question='How are you'),
            option_code='a',
            option_detail='great'
        )

        self.record = models.VoteRecord.objects.create(
            campaign=models.VoteCampaign.objects.get(question='How are you'),
            option=models.VoteOption.objects.get(option_detail='great'),
            user_id='A1234567'
        )

    def test_can_get_all_campaign(self):
        response = self.client.get(reverse('campaign_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.campaigns))
    
    def test_can_get_vote_count(self):
        response = self.client.get(reverse('campaign_list'))
        data = response.data
        campaign = [campaign for campaign in data if campaign['campaign_id'] == self.campaigns[0].campaign_id]
        self.assertEqual(len(campaign), 1)
        self.assertEqual(campaign[0]['number_of_vote'], 1)


class TestCampaignDetailRetrieveView(APITestCase):
    multi_db = True

    def setUp(self):
        self.campaign = models.VoteCampaign.objects.create(
            question='How are you',
            start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
            end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)                
        )

        self.options = models.VoteOption.objects.bulk_create([
            models.VoteOption(
                campaign=self.campaign,
                option_code='a',
                option_detail='great'
            ),
            models.VoteOption(
                campaign=self.campaign,
                option_code='b',
                option_detail='not great'
            ),
        ])

        self.record = models.VoteRecord.objects.create(
            campaign=self.campaign,
            option=self.options[0],
            user_id='A1234567'
        )

    def test_can_get_corresponding_campaign(self):
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.campaign_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['campaign_id'], self.campaign.campaign_id)

    def test_can_get_return_error_if_campaign_id_not_found(self):
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.campaign_id+1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data['detail']), 'NOT_FOUND')

    def test_can_get_return_corresponding_options(self):
        expected_options = set([option.option_code for option in self.options])
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.campaign_id]))
        response_options = set([option['option_code'] for option in response.data['options']])
        self.assertEqual(response_options, expected_options)
    
    def test_can_get_return_corresponding_options_with_correct_order(self):
        expected_options = sorted([option.option_code for option in self.options])
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.campaign_id]))
        response_options = [option['option_code'] for option in response.data['options']]
        self.assertEqual(response_options, expected_options)

    def test_can_get_count_per_vote_option(self):
        expected_vote_count = [len(option.record_set.all()) for option in self.options]
        response = self.client.get(reverse('campaign_detail', args=[self.campaign.campaign_id]))
        response_vote_count = [option['number_of_vote'] for option in response.data['options']]
        self.assertEqual(response_vote_count, expected_vote_count)


class TestVoteRecordView(APITestCase):
    multi_db = True

    def setUp(self):
        self.campaigns = models.VoteCampaign.objects.bulk_create([
            models.VoteCampaign(
                question='How old are you',
                start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)   
            ),
            models.VoteCampaign(
                question='How are you',
                start_time=datetime.datetime(2000, 1, 1, 0, 0, 0),
                end_time=datetime.datetime(2000, 2, 1, 0, 0, 0)   
            )
        ])

        self.options = models.VoteOption.objects.bulk_create([
            models.VoteOption(
                campaign=self.campaigns[0],
                option_code='a',
                option_detail='great'
            ),
            models.VoteOption(
                campaign=self.campaigns[0],
                option_code='b',
                option_detail='not great'
            ),
            models.VoteOption(
                campaign=self.campaigns[1],
                option_code='c',
                option_detail='18'
            ),
        ])

        self.record = models.VoteRecord.objects.create(
            campaign=self.campaigns[0],
            option=self.options[0],
            user_id='Y7280422'
        )

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_insert_new_vote(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943', 'option_code': 'b'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_already_voted(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Y7280422', 'option_code': 'b'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'ALREADY_VOTE')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 2, 1, 0, 0, 0))
    def test_can_prevent_vote_if_vote_already_closed(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943', 'option_code': 'b'}
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(1999, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_vote_not_yet_start(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943', 'option_code': 'b'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_campaign_not_exist(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id+1000]),
            data={'hkid': 'Q7853943', 'option_code': 'b'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_data_not_enough(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_option_not_match_campaign(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943', 'option_code': 'c'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')

    @patch('django.utils.timezone.now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0))
    def test_can_prevent_vote_if_option_not_exist(self, mock_datetime):
        response = self.client.post(
            reverse('vote', args=[self.campaigns[0].campaign_id]),
            data={'hkid': 'Q7853943', 'option_code': 'z'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['detail']), 'INVALID_INPUT')
