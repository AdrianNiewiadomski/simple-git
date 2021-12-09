import unittest

from simple_git.simple_git import SimplegitRunner


class TestSimplegitRunner(unittest.TestCase):
    def test_validate_command_line_arguments_no_arguments(self):
        simplegit_runner = SimplegitRunner()
        self.assertFalse(simplegit_runner._validate_command_line_arguments([]))

    def test_validate_command_line_arguments_not_enough_args(self):
        simplegit_runner = SimplegitRunner()
        self.assertFalse(simplegit_runner._validate_command_line_arguments(['path']))

    def test_validate_command_line_arguments_add_without_args(self):
        simplegit_runner = SimplegitRunner()
        self.assertFalse(simplegit_runner._validate_command_line_arguments(['path', 'add']))

    def test_validate_command_line_arguments_init_with_args(self):
        simplegit_runner = SimplegitRunner()
        self.assertFalse(simplegit_runner._validate_command_line_arguments(['path', 'init', 'bad_arg']))

    def test_validate_command_line_arguments_add_with_args(self):
        simplegit_runner = SimplegitRunner()
        self.assertTrue(simplegit_runner._validate_command_line_arguments(['path', 'add', 'file1']))

    def test_validate_command_line_arguments_init_with_args(self):
        simplegit_runner = SimplegitRunner()
        self.assertTrue(simplegit_runner._validate_command_line_arguments(['path', 'init']))
