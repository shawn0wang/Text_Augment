import json
import os
from typing import List

from .base_loader import Data, DataLoader


class DemoDataLoader(DataLoader):
    def __init__(self, data_name, save_file_name):
        super(DemoDataLoader, self).__init__(save_file_name)
        self.data_name = data_name
        self.data_path = os.path.join(self.data_dir, data_name)

    def read_data(self) -> List[Data]:
        all_data = []
        with open(self.data_path, "r", encoding="UTF-8") as f:
            for idx, data in enumerate(f.readlines()):
                json_data = json.loads(data)
                sentence = json_data["sentence"]
                all_data.append(
                    Data(data_id=str(idx), sentence=sentence, from_file=self.data_name)
                )
        return all_data
