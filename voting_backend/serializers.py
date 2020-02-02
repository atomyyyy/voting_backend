from rest_framework import serializers

from .models import VoteCampaign, VoteOption, VoteRecord


class VoteCampaignListSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    number_of_vote = serializers.IntegerField()

    class Meta:
        model = VoteCampaign
        fields = (
            'campaign_id',
            'question',
            'start_time',
            'end_time',
            'status',
            'number_of_vote'
        )


class VoteOptionSerializer(serializers.ModelSerializer):
    number_of_vote = serializers.IntegerField()

    class Meta:
        model = VoteOption
        fields = ('option_code', 'option_detail', 'number_of_vote')


class VoteCampaignDetailSerializer(VoteCampaignListSerializer):
    status = serializers.CharField()
    options = VoteOptionSerializer(source='option_set', many=True)

    class Meta(VoteCampaignListSerializer.Meta):
        fields = (
            'campaign_id',
            'question',
            'start_time',
            'end_time',
            'status',
            'options'           
        )


class VoteRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField()
    class Meta:
        model = VoteRecord
        fields = ('create_time',)
