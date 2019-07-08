import unittest
from .movie import Movie


class MyTestCase(unittest.TestCase):

    def test_movie_url(self):
        test_movie = Movie("tt0448157")
        self.assertEqual("https://www.imdb.com/title/tt0448157", test_movie.url)

    def test_movie_name(self):
        test_movie = Movie("tt0448157")
        self.assertEqual("Hancock", test_movie.name)

    def test_actor_image(self):
        test_movie = Movie("tt0448157")
        self.assertEqual("https://m.media-amazon.com/images/M/MV5BMTgyMzc4ODU3NV5BMl5BanBnXkFtZTcwNjk5Mzc1MQ@@._V1_.jpg",
                         test_movie.image)

    def test_movie_cast(self):
        test_movie = Movie("tt0448157")
        self.assertIn("https://www.imdb.com//name/nm0000226", test_movie.cast_list)


if __name__ == '__main__':
    unittest.main()
