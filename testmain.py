import os
import unittest
from main import app
from main import searchdb
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    #go to home page
    def test_home(self):
        home = self.app.get('/')
        self.assertTrue('TeamA7 Project Home' in str(home.data))

    #test seardb nonrealwords returns nothing
    def test_bad_search(self):
        exact, partial = searchdb('zxcvbnmasdfghjklqwertyuiop', {'boardgames': True, 'genres': True, 'publishers': True}, ['all'])
        self.assertEqual(partial,{'boardgames': [], 'genres': [], 'publishers': []})
        self.assertEqual(exact, [])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
