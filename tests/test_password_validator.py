import unittest

from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):

    def test_valid_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    def test_length_7(self):
        self.assertFalse(validate_password("Abc1!de"))

    def test_length_8(self):
        self.assertTrue(validate_password("Abc1!def"))

    def test_length_20(self):
        self.assertTrue(validate_password("Abcdefghij1!Abcdefgh"))

    def test_length_21(self):
        self.assertFalse(validate_password("Abcdefghij1!Abcdefghi"))

    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_underscore(self):
        self.assertFalse(validate_password("SecurePass1_"))

    def test_invalid_special_question(self):
        self.assertFalse(validate_password("SecurePass1?"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))

    def test_space_inside(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_space_start(self):
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_space_end(self):
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_type_none(self):
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_type_int(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_type_list(self):
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])


if __name__ == "__main__":
    unittest.main()