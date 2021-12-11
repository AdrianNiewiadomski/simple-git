from exception import MethodCalledException


class SimplegitMock:
    def __init__(self):
        pass

    @staticmethod
    def initialize_repozitory():
        raise MethodCalledException("initialize_repozitory called")

    @staticmethod
    def add_files(parameters):
        raise MethodCalledException(f"add_files called with {parameters}")
