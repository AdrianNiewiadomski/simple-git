import os
import shutil


class Simplegit:
    @staticmethod
    def initialize_repozitory():
        if os.path.exists(".simplegit"):
            shutil.rmtree(".simplegit", ignore_errors=True)

        os.mkdir(".simplegit")
        with open(".simplegit/reflog.txt", "w") as file:
            file.write("")

    @staticmethod
    def add_files(parameters):
        pass

    @staticmethod
    def commit_changes():
        pass

    @staticmethod
    def status():
        pass
