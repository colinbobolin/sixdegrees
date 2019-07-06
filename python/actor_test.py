import unittest
from .actor import Actor


class MyTestCase(unittest.TestCase):

    def test_actor_name(self):
        test_actor = Actor('https://www.imdb.com//name/nm0000226')
        self.assertEqual(test_actor.name, "Will Smith")

    def test_actor_movies(self):
        test_actor = Actor('https://www.imdb.com//name/nm0000226')
        self.assertIn("Aladdin", test_actor.movies_acted_in)


if __name__ == '__main__':
    unittest.main()
