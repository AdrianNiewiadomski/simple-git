import os


class SimplegitRunner:
    supported_commands = {
        "init",
        "add",
        "commit",
        "status"
    }

    def __init__(self, args: list):
        self.command = None
        self.parameters = None
        self._get_command_and_parameters_from_command_line_arguments(args)

    def _get_command_and_parameters_from_command_line_arguments(self, args: list):
        if SimplegitRunner._validate_command_line_arguments(args):

            self.command = args[1]
            self.parameters = args[2:]
            print("command: ", self.command)
            print("parameters: ", str(self.parameters))

    @staticmethod
    def _validate_command_line_arguments(args: list) -> bool:
        if len(args) < 2 or args[1] not in SimplegitRunner.supported_commands:
            SimplegitRunner.display_help()
        elif args[1] == "add" and len(args) < 3:
            print("Simplegit add command must be run with parameters!")
        elif len(args) > 2:
            print("Simplegit init, commit and status commands must be run without parameters!")
        else:
            return True
        return False

    @staticmethod
    def display_help():
        info_file_path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind("/")] + "/help/info.txt"
        print("info_file_path: ", info_file_path)
        with open(info_file_path, "r") as file:
            print(file.read())

    def run(self):
        pass
