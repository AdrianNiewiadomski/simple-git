import unittest

from simple_git.simple_git import Simplegit


class TestSimplegit(unittest.TestCase):
    def test_initialize_repozitory(self):
        pass

    def add_files(self):
        pass

    def commit_changes(self):
        pass

    def status(self):
        pass

    def test_get_recorded_files(path):
        print(Simplegit._get_recorded_files("test_data/.simplegit/stage.txt"))