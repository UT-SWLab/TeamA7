
import unittest
from main import app
from main import searchdb


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search(self):
        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        print(search)
        self.assertTrue(len(search['boardgames']) == 1)
        self.assertTrue(len(search['publishers']) == 0)
        self.assertTrue(len(search['genres']) == 0)

        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        print(search)
        self.assertTrue(len(search['boardgames']) == 1)
        self.assertTrue(len(search['publishers']) == 0)
        self.assertTrue(len(search['genres']) == 0)

        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        print(search)
        self.assertTrue(len(search['boardgames']) == 1)
        self.assertTrue(len(search['publishers']) == 0)
        self.assertTrue(len(search['genres']) == 0)

        search, search2 = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        print(search)
        self.assertTrue(len(search['boardgames']) == 1)
        self.assertTrue(len(search['publishers']) == 0)
        self.assertTrue(len(search['genres']) == 0)

        # self.assertTrue('TeamA7 Project Home' in str(home.data))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
