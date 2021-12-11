import unittest

from simple_git.simple_git import Simplegit, NothingToCommitException


class TestSimplegit(unittest.TestCase):
    # def test_initialize_repozitory(self):
    #     pass

    def add_files(self):
        pass

    def commit_changes(self):
        pass

    def status(self):
        pass

    # def test_get_recorded_files(path):
    #     print(Simplegit._get_recorded_files("test_data/.simplegit/stage.txt"))

    def test_analyze_files_nothing_to_commit(self):
        some_dict = {'a': 1, 'b': 2}
        with self.assertRaises(NothingToCommitException):
            Simplegit._analyze_files(some_dict, some_dict, {})

    def test_analyze_files_new_files(self):
        result = Simplegit._analyze_files({"a": "1", "b": "2"}, {}, {})
        self.assertEqual((["a", "b"], [], []), result)

    def test_analyze_files_staged_files(self):
        result = Simplegit._analyze_files(current_files={"a": "1"}, repository_files={}, staged_files={"a": "1"})
        self.assertEqual(([], ["a"], []), result)

    def test_analyze_files_modified_files(self):
        result = Simplegit._analyze_files(current_files={"a": "1"}, repository_files={"a": "2"}, staged_files={})
        self.assertEqual(([], [], ["a"]), result)
