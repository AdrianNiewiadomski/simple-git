import os
import shutil
import hashlib


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
            current_files = {path: Simplegit.get_digest(path) for path in all_paths}

            repository_files = Simplegit._get_recorded_files('.simplegit/repository.txt')
            staged_files = Simplegit._get_recorded_files('.simplegit/stage.txt')

            new, staged, modified = Simplegit._analyze_files(current_files, repository_files, staged_files)
            Simplegit._display_analysis_result(new, staged, modified)

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
        return {file.strip().split(" : ")[0]: file.strip().split(" : ")[1] for file in files}

    @staticmethod
    def _analyze_files(current_files, repository_files, staged_files):
        new = []
        staged = []
        modified = []

        if current_files == repository_files and not bool(staged_files):
            print("Nothing to commit")
            return
        else:
            for k, v in current_files.items():
                if k not in repository_files and k not in staged_files:
                    new.append(k)
                elif k in staged_files and current_files[k] == staged_files[k]:
                    staged.append(k)
                elif k not in staged_files and k in repository_files and current_files[k] != repository_files[k]:
                    modified.append(k)

        return new, staged, modified

    @staticmethod
    def _display_analysis_result(new, staged, modified):
        def display_result(file_list, name):
            for file in file_list:
                print(f"> {file} ({name} file)")

        display_result(new, "new")
        display_result(staged, "staged")
        display_result(modified, "modified")






    @staticmethod
    def add_files(parameters):
        pass

    @staticmethod
    def commit_changes():
        pass
