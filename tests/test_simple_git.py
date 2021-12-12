import os
import shutil
import unittest
from unittest.mock import patch

from simple_git.simple_git import Simplegit, NothingToCommitException


class TestSimplegit(unittest.TestCase):
    EMPTY_FILE_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def tearDown(self) -> None:
        current_dir = os.getcwd()
        if "/test_data" not in current_dir:
            current_dir = current_dir + "/test_data"
        for file in os.listdir(current_dir):
            try:
                os.remove(current_dir + "/" + file)
            except IsADirectoryError:
                shutil.rmtree(current_dir + "/" + file, ignore_errors=True)

    def test_initialize_repozitory(self):
        self._change_execution_directory()
        shutil.rmtree(".simplegit", ignore_errors=True)

        self.assertFalse(os.path.exists(".simplegit"))
        Simplegit.initialize_repozitory()
        self.assertTrue(os.path.exists(".simplegit/stage.txt"))
        self.assertTrue(os.path.exists(".simplegit/repository.txt"))

    @staticmethod
    def _change_execution_directory():
        current_dir = os.getcwd()
        if "/test_data" not in current_dir:
            os.chdir(current_dir + "/test_data")

    def test_initialize_repozitory_not_empty(self):
        self._change_execution_directory()
        if not os.path.exists(".simplegit"):
            os.mkdir(".simplegit")

        Simplegit.initialize_repozitory()
        self.assertTrue(os.path.exists(".simplegit/stage.txt"))
        self.assertTrue(os.path.exists(".simplegit/repository.txt"))

    def test_status(self):
        self._change_execution_directory()

        Simplegit.initialize_repozitory()
        Simplegit._create_empty_file("file1.txt")
        Simplegit._create_empty_file("file2.txt")
        Simplegit._create_empty_file("file3.txt")
        Simplegit._create_empty_file("file4.txt")

        # Let's say that file1 already has been committed.
        with open(".simplegit/repository.txt", "w") as f:
            f.write("file1.txt" + " : " + self.EMPTY_FILE_HASH + "\n")
            f.write("file2.txt" + " : " + self.EMPTY_FILE_HASH + "\n")

        # file2 has been modified.
        with open("file2.txt", "w") as f:
            f.write("some data")

        # file3 is staged and file4 is new.
        with open(".simplegit/stage.txt", "w") as f:
            f.write("file3.txt" + " : " + self.EMPTY_FILE_HASH + "\n")

        with patch.object(Simplegit, "_display_analysis_result") as mock_display_analysis_result:
            Simplegit.status()

        self.assertEqual(mock_display_analysis_result.call_args[0][0], ["file4.txt"])
        self.assertEqual(mock_display_analysis_result.call_args[0][1], ["file3.txt"])
        self.assertEqual(mock_display_analysis_result.call_args[0][2], ["file2.txt"])

    def test_analyze_files_nothing_to_commit(self):
        some_dict = {'a': 1, 'b': 2}
        with self.assertRaises(NothingToCommitException):
            Simplegit._analyze_files(current_files=some_dict, repository_files=some_dict, staged_files={})

    def test_analyze_files_new_files(self):
        result = Simplegit._analyze_files(current_files={"a": "1", "b": "2"}, repository_files={}, staged_files={})
        self.assertEqual((["a", "b"], [], []), result)

    def test_analyze_files_staged_files(self):
        result = Simplegit._analyze_files(current_files={"a": "1"}, repository_files={}, staged_files={"a": "1"})
        self.assertEqual(([], ["a"], []), result)

    def test_analyze_files_modified_files(self):
        result = Simplegit._analyze_files(current_files={"a": "1"}, repository_files={"a": "2"}, staged_files={})
        self.assertEqual(([], [], ["a"]), result)

    def test_add_files_all(self):
        self._prepare_test_data_for_add_files_test()
        Simplegit.add_files(["*"])
        self._check_results_of_add_files()

    def _prepare_test_data_for_add_files_test(self):
        self._change_execution_directory()
        Simplegit.initialize_repozitory()
        Simplegit._create_empty_file("file1.txt")
        Simplegit._create_empty_file("file2.txt")

        with open(".simplegit/stage.txt", "w") as f:
            f.write("file1.txt" + " : " + "some_hash" + "\n")

    def _check_results_of_add_files(self):
        with open(".simplegit/stage.txt", "r") as f:
            files = f.readlines()

        expected = {f"file1.txt : {self.EMPTY_FILE_HASH}\n", f"file2.txt : {self.EMPTY_FILE_HASH}\n"}
        self.assertEqual(set(files), expected)

    def test_add_files_list(self):
        self._prepare_test_data_for_add_files_test()
        Simplegit.add_files(["file1.txt", "file2.txt", "bad_file"])
        self._check_results_of_add_files()

    def test_commit_changes(self):
        self._change_execution_directory()
        Simplegit.initialize_repozitory()

        with open(".simplegit/stage.txt", "w") as f:
            f.write("file1.txt" + " : " + "some_hash" + "\n")

        Simplegit.commit_changes()

        with open(".simplegit/stage.txt", "r") as f:
            stage_after_commit = f.read()
            self.assertEqual(stage_after_commit, "")

        with open(".simplegit/repository.txt", "r") as f:
            repository_after_commit = f.read()
            self.assertEqual(repository_after_commit, "file1.txt : some_hash\n")
