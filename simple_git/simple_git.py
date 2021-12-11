import hashlib
import os
import shutil
from typing import Union


class NothingToCommitException(Exception):
    pass


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

        print("Initialized empty Git repository")

    @staticmethod
    def status() -> None:
        if not os.path.exists(".simplegit"):
            print("fatal: not a simplegit repository")
        else:
            current_files: dict = Simplegit._get_current_files()
            repository_files: dict = Simplegit._get_recorded_files('.simplegit/repository.txt')
            staged_files: dict = Simplegit._get_recorded_files('.simplegit/stage.txt')

            try:
                new, staged, modified = Simplegit._analyze_files(current_files, repository_files, staged_files)
                Simplegit._display_analysis_result(new, staged, modified)
            except NothingToCommitException:
                pass

    @staticmethod
    def _get_current_files() -> dict:
        all_paths: list = Simplegit._get_all_paths()
        return {path: Simplegit._get_file_hash(path) for path in all_paths}

    @staticmethod
    def _get_all_paths() -> list:
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
    def _get_file_hash(file_path: str) -> str:
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
    def _get_recorded_files(path) -> dict:
        with open(path, 'r') as f:
            files = f.readlines()
        return {file.strip().split(" : ")[0]: file.strip().split(" : ")[1] for file in files}

    @staticmethod
    def _analyze_files(current_files, repository_files, staged_files) -> Union[None, tuple]:
        new = []
        staged = []
        modified = []

        if current_files == repository_files and not bool(staged_files):
            print("Nothing to commit")
            raise NothingToCommitException
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
    def _display_analysis_result(new, staged, modified) -> None:
        def display_result(file_list, name):
            for file in file_list:
                print(f"> {file} ({name} file)")

        display_result(modified, "modified")
        display_result(staged, "staged")
        display_result(new, "new")

    @staticmethod
    def add_files(parameters: list) -> None:
        if len(parameters) == 1 and parameters[0] == "*":
            files_to_add: dict = Simplegit._get_current_files()
        else:
            files_to_add = {}
            for file in parameters:
                if os.path.exists(file):
                    files_to_add[file] = Simplegit._get_file_hash(file)
                else:
                    print(f"Warning! {file} does not exists.")

        Simplegit._add_all_files(files_to_add)

    @staticmethod
    def _add_all_files(files_to_add: dict) -> None:
        staged_files: dict = Simplegit._get_recorded_files('.simplegit/stage.txt')

        for k, v in staged_files.items():
            if k not in files_to_add:
                files_to_add[k] = v

        with open(".simplegit/stage.txt", "w") as file:
            for k, v in files_to_add.items():
                file.write(k + " : " + v + "\n")

    @staticmethod
    def commit_changes():
        staged_files: dict = Simplegit._get_recorded_files('.simplegit/stage.txt')
        repository_files: dict = Simplegit._get_recorded_files('.simplegit/repository.txt')

        for k, v in repository_files.items():
            if k not in staged_files:
                staged_files[k] = v

        with open(".simplegit/stage.txt", "w") as file:
            file.write("")

        with open(".simplegit/repository.txt", "w") as file:
            for k, v in staged_files.items():
                file.write(k + " : " + v + "\n")
