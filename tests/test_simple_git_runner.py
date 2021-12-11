import unittest
from unittest.mock import patch

from exception import MethodCalledException
from simple_git_mock import SimplegitMock
from simple_git.simple_git_runner import SimplegitRunner


class TestSimplegitRunner(unittest.TestCase):
    simplegit_runner = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.my_mock = SimplegitMock()
        cls.simplegit_runner = SimplegitRunner()
        cls.simplegit_runner.parameterless_commands = {"init": SimplegitMock.initialize_repozitory}
        cls.simplegit_runner.other_commands = {"add": SimplegitMock.add_files}

    def test_run_parameterless_commands(self):
        with self.assertRaises(MethodCalledException) as e:
            self.simplegit_runner.run(["a", "init"])
        self.assertEqual(str(e.exception), "initialize_repozitory called")

    def test_run_other_commands(self):
        with self.assertRaises(MethodCalledException) as e:
            self.simplegit_runner.run(["a", "add", "file1"])
        self.assertEqual(str(e.exception), "add_files called with ['file1']")

    def test_get_command_and_parameters_from_command_line_arguments(self):
        with patch("simple_git.simple_git_runner.SimplegitRunner._validate_command_line_arguments") as mock:
            mock.return_value = True
            self.simplegit_runner._get_command_and_parameters_from_command_line_arguments([1, 2, 3])

            self.assertEqual(self.simplegit_runner.command, 2)
            self.assertEqual(self.simplegit_runner.parameters, [3])

    def test_validate_command_line_arguments_no_arguments(self):
        self.assertFalse(self.simplegit_runner._validate_command_line_arguments([]))

    def test_validate_command_line_arguments_not_enough_args(self):
        self.assertFalse(self.simplegit_runner._validate_command_line_arguments(['path']))

    def test_validate_command_line_arguments_add_without_args(self):
        self.assertFalse(self.simplegit_runner._validate_command_line_arguments(['path', 'add']))

    def test_validate_command_line_arguments_init_with_args(self):
        self.assertFalse(self.simplegit_runner._validate_command_line_arguments(['path', 'init', 'bad_arg']))

    def test_validate_command_line_arguments_add_with_args(self):
        self.assertTrue(self.simplegit_runner._validate_command_line_arguments(['path', 'add', 'file1']))

    def test_validate_command_line_arguments_init_without_args(self):
        self.assertTrue(self.simplegit_runner._validate_command_line_arguments(['path', 'init']))

    def test_display_help(self):
        with patch("builtins.open") as open_mock:
            self.simplegit_runner._display_help()

            self.assertEqual(open_mock.call_count, 1)
            self.assertTrue("simple_git/help/info.txt" in str(open_mock.call_args))
