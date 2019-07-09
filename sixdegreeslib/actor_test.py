import unittest
from .actor import Actor


class MyTestCase(unittest.TestCase):

    def test_actor_name(self):
        test_actor = Actor('nm0000226')
        self.assertEqual("Will Smith", test_actor.name)

    def test_actor_url(self):
        test_actor = Actor('nm0000226')
        self.assertEqual("https://www.imdb.com/name/nm0000226", test_actor.url)

    def test_actor_image(self):
        test_actor = Actor('nm0000226')
        self.assertEqual("https://m.media-amazon.com/images/"
                         "M/MV5BNTczMzk1MjU1MV5BMl5BanBnXkFtZTcwNDk2MzAyMg@@._V1_.jpg",
                         test_actor.image)

    #def test_actor_movies(self):
    #    test_actor = Actor('nm0000226')
    #    self.assertIn("https://www.imdb.com//title/tt6139732/", test_actor.movies)


if __name__ == '__main__':
    unittest.main()
