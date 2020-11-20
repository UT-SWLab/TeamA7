
import unittest
from main import app
from main import search


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search(self):
        search = self.app.get('/search')

        self.assertTrue('TeamA7 Project Home' in str(home.data))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
