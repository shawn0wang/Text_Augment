import json
from collections import defaultdict

from __init__ import func_loader
from data_loader import run_loader


class FileDataStruct:
    def __init__(self,
                 data_id: str,
                 raw_sentence: str,
                 func_name: str,
                 new_sentence: str,
                 from_file: str):
        self.data_id = self._check_valid(data_id, str)
        self.raw_sentence = self._check_valid(raw_sentence, str)
        self.func_name = self._check_valid(func_name, str)
        self.new_sentence = self._check_valid(new_sentence, str)
        self.from_file = self._check_valid(from_file, str)

    @staticmethod
    def _check_valid(value, type_name):
        if not isinstance(value, type_name):
            raise TypeError(f"{value} must be a {type_name}")
        else:
            return value


class Process:
    def __init__(self, data_loaders):
        self.data_loaders = data_loaders

    def process(self):
        for loader in self.data_loaders:
            data = loader.read_data()
            with open(f"{loader.save_file_path}", "w") as f:
                for item in data:
                    all_data_dict = defaultdict(FileDataStruct)

                    for func_name, func in func_loader:
                        func_result = func.process(item.sentence)
                        func_result = list(set(func_result))

                        for new_sentence in func_result:
                            all_data_dict[new_sentence] = FileDataStruct(
                                data_id=item.data_id,
                                raw_sentence=item.sentence,
                                func_name=func_name,
                                new_sentence=new_sentence,
                                from_file=item.from_file)

                    for new_sentence in all_data_dict.keys():
                        if new_sentence != item.sentence:
                            f.write(json.dumps(all_data_dict[new_sentence].__dict__, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    Process(data_loaders=run_loader).process()
