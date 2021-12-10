import os
import shutil
import stat
import time
import hashlib


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
            print(path, " : ", time.ctime(os.stat(path)[stat.ST_MTIME]), " : ", Simplegit.get_digest(path))

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

    @staticmethod
    def get_digest(file_path):
        h = hashlib.sha256()

        with open(file_path, 'rb') as file:
            while True:
                # Reading is buffered, so we can read smaller chunks.
                chunk = file.read(h.block_size)
                if not chunk:
                    break
                h.update(chunk)

        return h.hexdigest()