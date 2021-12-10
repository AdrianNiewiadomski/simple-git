import os
import shutil
import hashlib

# from .file import File


class Simplegit:
    @staticmethod
    def initialize_repozitory():
        if os.path.exists(".simplegit"):
            shutil.rmtree(".simplegit", ignore_errors=True)

        os.mkdir(".simplegit")
        with open(".simplegit/stage.txt", "w") as file:
            file.write("")
        with open(".simplegit/repository.txt", "w") as file:
            file.write("")

    @staticmethod
    def status():
        if not os.path.exists(".simplegit"):
            print("fatal: not a simplegit repository")
        else:
            all_paths = Simplegit._get_all_paths()
            current_files = {(path, Simplegit.get_digest(path)) for path in all_paths}
            # current_files = [File(path, Simplegit.get_digest(path)) for path in all_paths]
            # current_files = {str(file) for file in current_files}

            print("current_files:")
            print(type(current_files))
            for item in current_files:
                print(item)

            print("staged_files:")
            staged_files = Simplegit._get_recorded_files('.simplegit/stage.txt')
            # staged_files = [File.create_from_string(file) for file in staged_files]
            # staged_files = {str(file) for file in staged_files}

            print(type(staged_files))
            for item in staged_files:
                print(item)

    @staticmethod
    def _get_all_paths():
        all_paths = []
        for file_names in os.walk("."):
            if file_names[0].find(".simplegit") == -1:
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

    @staticmethod
    def _get_recorded_files(path):
        with open(path, 'r') as f:
            files = f.readlines()
        # return files
        return {tuple(file.strip().split(" : ")) for file in files}
    #
    # "123 : abc\n".strip().split(" : ")
    # ['123', 'abc']

    @staticmethod
    def add_files(parameters):
        pass

    @staticmethod
    def commit_changes():
        pass