import yaml

from function.abbreviation_func import AbbreviationFunc
from function.antonym_func import AntonymFunc
from function.deletion_func import DeletionFunc
from function.gpt_35_func import Gpt35Func
from function.gpt_3_func import Gpt3Func
from function.insertion_func import InsertionFunc
from function.ner_func import NerFunc
from function.seq2seq_sim_func import Seq2SeqSimFunc
from function.simplified_traditional_func import SimplifiedTraditionalFunc
from function.swap_func import SwapFunc
from function.synonyms_func import SynonymsFunc
from function.translate_func import TranslateFunc

func_obj = {
    "abbreviation_func": AbbreviationFunc,
    "antonym_func": AntonymFunc,
    "deletion_func": DeletionFunc,
    "gpt_3_func": Gpt3Func,
    "gpt_35_func": Gpt35Func,
    "insertion_func": InsertionFunc,
    "ner_func": NerFunc,
    "seq2seq_sim_func": Seq2SeqSimFunc,
    "simplified_traditional_func": SimplifiedTraditionalFunc,
    "swap_func": SwapFunc,
    "synonyms_func": SynonymsFunc,
    "translate_func": TranslateFunc
}


class CallableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = CallableDict(value)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __call__(self, *args, **kwargs):
        return self


func_loader = []
with open("config.yaml", "r", encoding="UTF-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    for func_name in config.keys():
        if func_name in func_obj and config[func_name]["use"]:
            func_loader.append((func_name, func_obj[func_name](CallableDict(**config))))
