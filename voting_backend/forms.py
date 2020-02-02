import re

from django import forms
from django.core.exceptions import ValidationError


class HKIDField(forms.CharField):
    """
    Custom field to check if the id is valid HKID
    """
    @staticmethod
    def id_char_to_value(char):
        try:
            digit_value = int(char)
            return digit_value
        except ValueError:
            return ord(char) - ord('A') + 10

    @staticmethod
    def hkid_checksum(digit_sum, checksum):
        remainder = digit_sum % 11
        if remainder == 0 and checksum == 0:
            return True
        if remainder == 1 and checksum == 'A':
            return True
        if str(11-remainder) == checksum:
            return True
        return False
    
    def get_digit_sum(self, value):
        if len(value) == 9:
            return sum([(9-ix) * self.id_char_to_value(digit) for ix, digit in enumerate(value)])
        return  58*9 + sum([(8-ix)*self.id_char_to_value(digit) for ix, digit in enumerate(value)])

    def validate(self, value):
        super().validate(value)
        if not re.match('^([A-Z]{1,2})([0-9]{6})([A0-9])$', value):
            raise ValidationError(message='INCORRECT_PATTERN')
        digit_sum = self.get_digit_sum(value[:-1])
        if not self.hkid_checksum(digit_sum, value[-1]):
            raise ValidationError(message='INCORRECT_CHECKSUM')
    
    def prepare_value(self, value):
        if isinstance(value, str):
            return value.upper()
        return value


class VoteRecordForm(forms.Form):
    hkid = HKIDField()
    option_code = forms.CharField()
