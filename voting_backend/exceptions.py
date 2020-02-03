from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class InvalidFormException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('INVALID_INPUT')
    default_code = 'invalid'

class AlreadyVoteException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('ALREADY_VOTE')
    default_code = 'invalid'

class NotFoundException(exceptions.NotFound):
    default_detail = _('NOT_FOUND')


class InternalServerError(exceptions.APIException):
    default_detail = _('INTERNAL_SERVER_ERROR')
