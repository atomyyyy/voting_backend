from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count, Prefetch, prefetch_related_objects
from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                    RetrieveAPIView)
from rest_framework.response import Response

from .exceptions import (AlreadyVoteException, InternalServerError,
                        InvalidFormException, NotFoundException)
from .forms import VoteRecordForm
from .models import VoteCampaign, VoteOption, VoteRecord
from .serializers import (VoteCampaignDetailSerializer,
                        VoteCampaignListSerializer, VoteRecordSerializer)


class CampaignOverviewListView(ListAPIView):
    """
    List all voting campaign with total number of votes
    """
    serializer_class = VoteCampaignListSerializer
    model = VoteCampaign

    def get_queryset(self):
        queryset = self.model.objects.all().annotate(
            number_of_vote=Count('record_set')
        )
        return queryset


class CampaignDetailRetrieveView(RetrieveAPIView):
    """
    List Current Campaign Result
    """
    serializer_class = VoteCampaignDetailSerializer
    lookup_field = 'campaign_id'
    model = VoteCampaign
    queryset = VoteCampaign.objects.all()

    def get_object(self):
        # Leverage default get object logic for default lookup
        try:
            obj = super().get_object()
        except Http404:
            raise NotFoundException()
        except Exception:
            raise InternalServerError()
        prefetch_related_objects([obj], Prefetch(
            'option_set',
            queryset=VoteOption.objects.filter(
                campaign=obj
            ).order_by(
                'option_code'
            ).annotate(
                number_of_vote=Count('record_set')
            )
        ))
        return obj


class VoteRecordView(GenericAPIView):
    """
    Vote for certain Campaign
    """
    model = VoteRecord
    serializer = VoteRecordSerializer

    def post(self, request, *args, **kwargs):
        """
        1. Check if option and ID is included in POST form
        2. Check active campaign and option existent and the relation
        3. Save record
        """
        form = VoteRecordForm(request.POST)
        form.full_clean()
        if not form.is_valid():
            raise InvalidFormException()

        cleaned_data = form.cleaned_data
        try:
            campaign = VoteCampaign.objects.filter(end_time__gt=timezone.make_aware(timezone.now(), timezone.utc)).get(campaign_id=kwargs.get('campaign_id'))
            option = VoteOption.objects.filter(campaign=campaign).get(option_code=cleaned_data.get('option_code'))
            hkid = cleaned_data.get('hkid')
            instance = self.model(campaign=campaign, option=option, user_id=hkid)
            instance.save()
            return Response(self.serializer(instance).data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            raise InvalidFormException()
        except IntegrityError:
            raise AlreadyVoteException()
        except Exception:
            raise InternalServerError()
