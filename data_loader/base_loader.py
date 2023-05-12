import os
from abc import ABCMeta, abstractmethod
from typing import List


class Data:
    def __init__(self, data_id: str, sentence: str, from_file: str):
        self.data_id = self._check_valid(data_id, str)
        self.sentence = self._check_valid(sentence, str)
        self.from_file = self._check_valid(from_file, str)

    @staticmethod
    def _check_valid(value, type_name):
        if not isinstance(value, type_name):
            raise TypeError(f"{value} must be a {type_name}")
        else:
            return value


class DataLoader(metaclass=ABCMeta):
    def __init__(self, save_file_name: str):
        self.data_dir = os.path.join(os.getcwd(), "data_loader/data")
        self.save_file_path = os.path.join(os.getcwd(), "data_loader/augment_data", save_file_name)

    @abstractmethod
    def read_data(self) -> List[Data]:
        raise ValueError
