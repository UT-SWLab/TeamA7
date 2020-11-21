
import unittest
from main import app
from main import searchdb


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_exact_search(self):
        exact, partial = searchdb('Scrabble', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        print(exact)
        self.assertTrue(len(exact['boardgames']) == 1)
        self.assertTrue(len(exact['publishers']) == 0)
        self.assertTrue(len(exact['genres']) == 0)

        exact, partial = searchdb('Scrabble', {'boardgames': True, 'genres': False, 'publishers': False}, ['Name'])
        self.assertTrue(exact['boardgames'][0]['Name'] == 'Scrabble')

        exact, partial = searchdb('Racing', {'boardgames': False, 'genres': True, 'publishers': False}, ['Name'])
        self.assertTrue(exact['genres'][0]['Name'] == 'Racing')

        exact, partial = searchdb('Stronghold', {'boardgames': False, 'genres': False, 'publishers': True}, ['Name'])
        self.assertTrue(exact['publishers'][0]['Name'] == 'Stronghold Games')

        exact, partial = searchdb('Flamme Rouge', {'boardgames': False, 'genres': True, 'publishers': False}, ['Games'])
        self.assertTrue(exact['genres'][0]['Name'] == 'Racing')

        exact, partial = searchdb('Flamme Rouge', {'boardgames': False, 'genres': False, 'publishers': True}, ['Games'])
        self.assertTrue(exact['publishers'][0]['Name'] == 'Stronghold Games')

    def test_partial_search(self):
        exact, partial = searchdb('Flam asdfasdf', {'boardgames': True, 'genres': True, 'publishers': True}, ['Name'])
        self.assertTrue(len(partial['Flam']['boardgames']) == 1)
        self.assertTrue(len(partial['Flam']['publishers']) == 0)
        self.assertTrue(len(partial['Flam']['genres']) == 0)

        exact, partial = searchdb('Scrab safsddf', {'boardgames': True, 'genres': False, 'publishers': False}, ['Name'])
        self.assertEqual(partial['Scrab']['boardgames'][0]['Name'], 'Scrabble')

        exact, partial = searchdb('Rac sdfsaf', {'boardgames': False, 'genres': True, 'publishers': False}, ['Name'])
        self.assertEqual(partial['Rac']['genres'][0]['Name'], 'Racing')

        exact, partial = searchdb('Strong asdfasdf', {'boardgames': False, 'genres': False, 'publishers': True}, ['Name'])
        self.assertEqual(partial['Strong']['publishers'][0]['Name'], 'Stronghold Games')

        exact, partial = searchdb('Flam asdfasdf', {'boardgames': False, 'genres': True, 'publishers': False}, ['Games'])
        self.assertEqual(partial['Flam']['genres'][0]['Name'], 'Racing')

        exact, partial = searchdb('Flam asdfasdf', {'boardgames': False, 'genres': False, 'publishers': True}, ['Games'])
        self.assertEqual(partial['Flam']['publishers'][0]['Name'], 'Stronghold Games')

    def test_bad_search(self):
        exact, partial = searchdb('zxcvbnmasdfghjklqwertyuiop',
                                  {'boardgames': True, 'genres': True, 'publishers': True}, ['all'])
        self.assertEqual(exact, {'boardgames': [], 'genres': [], 'publishers': []})
        self.assertEqual(partial, {})

    def test_fields(self):
        exact, partial = searchdb('Scrabble', {'boardgames': True, 'genres': False, 'publishers': False}, ['Name'])
        self.assertTrue(len(exact) == 1)

        exact, partial = searchdb('Scrabble', {'boardgames': False, 'genres': True, 'publishers': True}, ['Name'])
        self.assertTrue(len(exact) == 2)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
