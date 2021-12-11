import os

from simple_git import Simplegit


class SimplegitRunner:
    parameterless_commands = {
        "init": Simplegit.initialize_repozitory,
        "commit": Simplegit.commit_changes,
        "status": Simplegit.status
    }
    other_commands = {
        "add": Simplegit.add_files
    }

    def __init__(self):
        self.command = None
        self.parameters = None

    def run(self, args: list) -> None:
        self._get_command_and_parameters_from_command_line_arguments(args)
        if self.command in self.parameterless_commands:
            SimplegitRunner.parameterless_commands[self.command]()
        elif self.command in self.other_commands:
            SimplegitRunner.other_commands[self.command](self.parameters)

    def _get_command_and_parameters_from_command_line_arguments(self, args: list) -> None:
        if SimplegitRunner._validate_command_line_arguments(args):
            self.command = args[1]
            self.parameters = args[2:]

    @staticmethod
    def _validate_command_line_arguments(args: list) -> bool:
        if len(args) <= 1 or args[1] not in SimplegitRunner.parameterless_commands.keys() and args[1] not in \
                SimplegitRunner.other_commands.keys():
            SimplegitRunner._display_help()
        elif args[1] in SimplegitRunner.other_commands.keys() and len(args) < 3:
            print("Simplegit add command must be run with parameters!")
        elif args[1] in SimplegitRunner.parameterless_commands and len(args) > 2:
            print("Simplegit init, commit and status commands must be run without parameters!")
        else:
            return True
        return False

    @staticmethod
    def _display_help() -> None:
        info_file_path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind("/")] + "/help/info.txt"
        with open(info_file_path, "r") as file:
            print(file.read())
