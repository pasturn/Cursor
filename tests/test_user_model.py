__author__ = 'Pasturn'
import  unittest
from app.models import Users

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = Users(password = 'abcdefg')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = Users(password = 'abcdefg')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verfication(self):
        u = Users(password = 'abcdefg')
        self.assertTrue(u.verify_password('abcdefg'))
        self.assertFalse(u.verify_password('gfedcba'))

    def test_password_salts_are_random(self):
        u = Users(password = 'abcdefg')
        u2 = Users(password = 'abcdefg')
        self.assertTrue(u.password_hash != u2.password_hash)
