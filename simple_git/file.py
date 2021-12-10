class File:
    def __init__(self, path, file_hash):
        self.path = path
        self.hash = file_hash

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path and self.hash == other.hash
        return False

    def __str__(self):
        return self.path + " : " + self.hash

    @staticmethod
    def create_from_string(file_info: str):
        file = file_info.strip().split(" : ")
        print(file)
        return File.__init__(File, file[0], file[1])
