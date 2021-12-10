import os
import shutil
import stat
import time


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
        all_paths = Simplegit._get_all_paths()
        for path in all_paths:
            print(path, ":", time.ctime(os.stat(path)[ stat.ST_MTIME ]))

    @staticmethod
    def _get_all_paths():
        all_paths = []
        for file_names in os.walk("."):
            all_paths.extend(Simplegit._get_paths(file_names))
        return all_paths

    @staticmethod
    def _get_paths(file_names: tuple) -> list:
        paths = []
        for file in file_names[2]:
            path = file_names[0] + "/" + file
            paths.append(path[2:])
        return paths
