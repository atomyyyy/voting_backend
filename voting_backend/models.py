from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class VoteCampaign(models.Model):
    """
    Model storing all campaigns hosted by the voting application
    """
    campaign_id = models.AutoField(primary_key=True)
    question = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.campaign_id}: {self.question}'
    
    @property
    def status(self):
        current_time = timezone.make_aware(timezone.now(), timezone.utc)
        if current_time < timezone.make_aware(self.start_time, timezone.utc):
            return 'NOT_START'
        if current_time >= timezone.make_aware(self.end_time, timezone.utc):
            return 'CLOSED'
        return 'ACTIVE'

    def save(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError(message='End time must be later than start time.')
        super().save(*args, **kwargs)


class VoteOption(models.Model):
    """
    Model storing all possible options per voting campaign
    """
    campaign = models.ForeignKey(VoteCampaign, on_delete=models.CASCADE, related_name='option_set')
    option_code = models.TextField()
    option_detail = models.TextField()

    def __str__(self):
        return f'{self.option_code}: {self.option_detail}'

    class Meta:
        unique_together = ('campaign', 'option_code')


class VoteRecord(models.Model):
    """
    Model storing all previous voting records
    """
    campaign = models.ForeignKey(VoteCampaign, on_delete=models.CASCADE, related_name='record_set')
    option = models.ForeignKey(VoteOption, on_delete=models.CASCADE, related_name='record_set')
    user_id = models.TextField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent muiltiple votes from same user in one campaign
        unique_together = ('user_id', 'campaign')
