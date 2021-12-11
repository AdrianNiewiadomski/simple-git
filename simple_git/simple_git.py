import hashlib
import os
import shutil
from typing import Union


class NothingToCommitException(Exception):
    pass


class Simplegit:
    @staticmethod
    def initialize_repozitory() -> None:
        if os.path.exists(".simplegit"):
            shutil.rmtree(".simplegit", ignore_errors=True)

        os.mkdir(".simplegit")
        Simplegit._create_empty_file(".simplegit/stage.txt")
        Simplegit._create_empty_file(".simplegit/repository.txt")

        print("Initialized empty Simplegit repository")

    @staticmethod
    def _create_empty_file(path: str) -> None:
        with open(path, "w") as file:
            file.write("")

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
        files_to_add = Simplegit._complete_dictionary(files_to_add, staged_files)
        Simplegit._save_dictionary_in_file(".simplegit/stage.txt", files_to_add)

    @staticmethod
    def _complete_dictionary(dict_1, dict_2) -> dict:
        for k, v in dict_2.items():
            if k not in dict_1:
                dict_1[k] = v
        return dict_1

    @staticmethod
    def _save_dictionary_in_file(path: str, dictionary: dict) -> None:
        with open(path, "w") as file:
            for k, v in dictionary.items():
                file.write(k + " : " + v + "\n")

    @staticmethod
    def commit_changes() -> None:
        staged_files: dict = Simplegit._get_recorded_files('.simplegit/stage.txt')
        repository_files: dict = Simplegit._get_recorded_files('.simplegit/repository.txt')

        staged_files = Simplegit._complete_dictionary(staged_files, repository_files)

        Simplegit._create_empty_file(".simplegit/stage.txt")
        Simplegit._save_dictionary_in_file(".simplegit/repository.txt", staged_files)
