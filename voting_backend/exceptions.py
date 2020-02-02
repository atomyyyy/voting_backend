from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class InvalidFormException(exceptions.ParseError):
    default_detail = _('INVALID_INPUT')


class AlreadyVoteException(exceptions.ParseError):
    default_detail = _('ALREADY_VOTE')


class NotFoundException(exceptions.NotFound):
    default_detail = _('NOT_FOUND')


class InternalServerError(exceptions.APIException):
    default_detail = _('INTERNAL_SERVER_ERROR')
