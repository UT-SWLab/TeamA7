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
        self.assertEqual(exact, {'boardgames': [], 'genres': [], 'publishers': []})
        self.assertEqual(partial, {})

    def test_game_list(self):
        self.app.get('/')
        gamelist = self.app.get('boardgames/normal/1/nofilters')
        self.assertEqual(gamelist.status_code, 200)
        self.assertTrue('Board Games Page 1' in gamelist.data)

    def test_genre_list(self):
        self.app.get('/')
        genrelist = self.app.get('boardgamegenres/normal/1/nofilters')
        self.assertEqual(gamelist.status_code, 200)
        self.assertTrue('Genres Page 1' in genrelist.data)

    def test_publisher_list(self):
        self.app.get('/')
        publisherlist = self.app.get('publishers/normal/1/nofilters')
        self.assertEqual(gamelist.status_code, 200)
        self.assertTrue('Publishers Page 1' in publisherlist.data)
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
