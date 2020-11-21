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

    #test game page is valid
    def test_game_list(self):
        gamelist = self.app.get('boardgames/normal/1/nofilters')
        self.assertEqual(gamelist.status_code, 200)
        #self.assertTrue('Board Games Page 1' in str(gamelist.data))

    #test genre page is valid
    def test_genre_list(self):
        genrelist = self.app.get('boardgamegenres/normal/1/nofilters')
        self.assertEqual(genrelist.status_code, 200)
        #self.assertTrue('Genres Page 1' in str(genrelist.data))

    #test publisher page is valid
    def test_publisher_list(self):
        publisherlist = self.app.get('boardgamepublishers/normal/1/nofilters')
        self.assertEqual(publisherlist.status_code, 200)
        #self.assertTrue('Publishers Page 1' in str(publisherlist.data))

    # test boardgame filter pages are valid
    def test_game_list_filters(self):
        filters = ['1_Hour_or_More',
                   '1_Hour_or_Less',
                   '30_Minutes_or_Less',
                   'Players:_2',
                   'Players:_3',
                   'Players:_4',
                   'Players:_5 +']
        for f in filters:
            filteredpage = self.app.get('boardgames/normal/1/'+f)
            self.assertEqual(filteredpage.status_code, 200)
            #self.assertTrue('Board Games Page 1' in str(filteredpage.data))

    # test genre filter pages are valid
    def test_genre_list_filters(self):
        filters = ['Average_Price:_$30_or_More',
                   'Average_Price:_$30_or_Less',
                   'Average_Price:_$15_or_Less',
                   'Average_Playtime:_30_minutes_or_Less',
                   'Average_Playtime:_30_Minutes_or_More']
        for f in filters:
                filteredpage = self.app.get('boardgamegenres/normal/1/' + f)
                self.assertEqual(filteredpage.status_code, 200)
                #self.assertTrue('Genres Page 1' in str(filteredpage.data))

    # test publisher filter pages are valid
    def test_publisher_list_filters(self):
        filters = ['Average_Price:_$30_or_More',
                   'Average_Price:_$30_or_Less',
                   'Average_Price:_$15_or_Less',
                   'Average_Playtime:_30_minutes_or_Less',
                   'Average_Playtime:_30_Minutes_or_More']
        for f in filters:
            filteredpage = self.app.get('boardgamepublishers/normal/1/' + f)
            self.assertEqual(filteredpage.status_code, 200)
            #self.assertTrue('Publishers Page 1' in str(filteredpage.data))

    # test games sort pages are valid
    def test_game_list_sort(self):
        sort = ["alphabetical","inverse","min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgames/'+s+'/1/nofilters')
            self.assertEqual(filteredpage.status_code, 200)
            #self.assertTrue('Board Games Page 1' in str(sortedpage.data))

    # test genres sort pages are valid
    def test_genres_list_sort(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgamegenres/' + s + '/1/nofilters')
            self.assertEqual(filteredpage.status_code, 200)
            #self.assertTrue('Genres Page 1' in str(sortedpage.data))

    # test publisher sort pages are valid
    def test_publishers_list_sort(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        for s in sort:
            sortedpage = self.app.get('boardgamepublishers/' + s + '/1/nofilters')
            self.assertEqual(filteredpage.status_code, 200)
            #self.assertTrue('Publishers Page 1' in str(sortedpage.data))

    # test game sort+filter pages are valid
    def test_game_list_sort_filter(self):
        sort = ["alphabetical", "inverse", "min-playtime", "min-players, normal"]
        filters = ['1_Hour_or_More',
                   '1_Hour_or_Less',
                   '30_Minutes_or_Less',
                   'Players:_2',
                   'Players:_3',
                   'Players:_4',
                   'Players:_5 +']
        for s in sort:
            for f in filters:
                sortedpage = self.app.get('boardgames/' + s + '/1/'+f)
                self.assertEqual(filteredpage.status_code, 200)
                #self.assertTrue('Board Games Page 1' in str(sortedpage.data))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
