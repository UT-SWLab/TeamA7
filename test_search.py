
import unittest
import main

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    #go to home page
    def test_search(self):
        home = self.app.get('/')
        self.assertTrue('TeamA7 Project Home' in str(home.data))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
