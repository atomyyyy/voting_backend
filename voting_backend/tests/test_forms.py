from unittest import TestCase

from django.core.exceptions import ValidationError

from voting_backend import forms


class TestHKIDField(TestCase):
    def setUp(self):
        self.field = forms.HKIDField()
    
    def test_can_identify_irrelevant_string(self):
        with self.assertRaises(ValidationError) as e:
            self.field.clean('!@#$%')
    
    def test_can_identify_hkid_with_invalid_checksum(self):
        with self.assertRaises(ValidationError):
            self.field.clean('Y728042A')
    
    def test_can_identify_hkid_with_valid_checksum(self):
        cleaned_value = self.field.clean('Y7280422')
        self.assertEqual(cleaned_value, 'Y7280422')


class TestVoteRecordForm(TestCase):
    form = forms.VoteRecordForm

    def test_can_identify_missing_input(self):
        test_form = self.form({'hkid': 'Y7280422'})
        test_form.full_clean()
        self.assertEqual(test_form.is_valid(), False)
