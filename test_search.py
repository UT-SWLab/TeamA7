
import unittest
from main import app
from main import searchdb


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search(self):
        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        self.assertTrue(len(search['boardgames']) == 1)
        self.assertTrue(len(search['publishers']) == 0)
        self.assertTrue(len(search['genres']) == 0)

        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': False, 'publishers': False}, ['Name'])
        self.assertTrue(search['boardgames'][0]['Name'] == 'Scrabble')

        search, search2 = searchdb('Racing', {'boardgames': False, 'genres': True, 'publishers': False}, ['Name'])
        self.assertTrue(search['genres'][0]['Name'] == 'Racing')

        search, search2 = searchdb('Stronghold', {'boardgames': False, 'genres': False, 'publishers': True}, ['Name'])
        self.assertTrue(search['publishers'][0]['Name'] == 'Stronghold Games')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
