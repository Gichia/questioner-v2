"""File to test all validations"""
from app.api.utils.validations import Validations
from app.tests.basetest import BaseTest

validate = Validations()

class TestValidations(BaseTest):
    """ Class to test all our validation methods"""

    def test_is_string(self):
        """Test to validate if value is string"""
        response = validate.is_string(1234)
        response1 = validate.is_string('hey')

        self.assertEqual(response, False)
        self.assertEqual(response1, True)

    def test_is_int(self):
        """Test to validate if value is integer"""
        response = validate.is_numeric(84849595)
        response1 = validate.is_numeric('hey')

        self.assertEqual(response, True)
        self.assertEqual(response1, False)

    def test_valid_email(self):
        """Test to validate email"""
        response = validate.is_valid_email('petergich')
        response1 = validate.is_valid_email('petergich@gmail.com')

        self.assertEqual(response, False)
        self.assertTrue(response1, True)

    def test_valid_password(self):
        """Test for validate password method"""
        response = validate.is_valid_password('1234y')
        response1 = validate.is_valid_password('@Petergich1')

        self.assertEqual(response, False)
        self.assertTrue(response1, True)
