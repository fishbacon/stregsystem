from django.test import TestCase
from fembers import utils


class TestGrouper(TestCase):
    pass


class TestMiscFunctions(TestCase):
    def test_phone_letter_converter_lower(self):
        self.assertEqual(utils.phone_letter_converter('5052treo'), '50528736')

    def test_phone_letter_converter_upper(self):
        self.assertEqual(utils.phone_letter_converter('5052TREO'), '50528736')

    def test_remove_sperators_success(self):
        self.assertEqual(utils.remove_seperators('._-', '_-.'), '')
