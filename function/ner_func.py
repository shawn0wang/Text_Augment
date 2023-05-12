import random
from collections import defaultdict

import torch
from ltp import LTP

from .base_func import BaseFunc


class NerFunc(BaseFunc):
    def __init__(self, config):
        super(NerFunc, self).__init__(config)
        self.augment_num = config.ner_func.augment_num
        self.combine_dict = self.load_ner_files()
        self.model = LTP(config.ner_func.ner_tool_name)
        if torch.cuda.is_available():
            self.model.to("cuda")

    @staticmethod
    def load_ner_files():
        combine_dict = defaultdict(set)
        # Nh file
        for line in open("files/ner/people_name.txt", "r", encoding="utf-8"):
            combine_dict["Nh"].add(line.strip())
        # Ns file
        for line in open("files/ner/place_name.txt", "r", encoding="utf-8"):
            combine_dict["Ns"].add(line.strip())
        # Ni file
        for line in open("files/ner/company_name.txt", "r", encoding="utf-8"):
            combine_dict["Ni"].add(line.strip())
        return combine_dict

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)
        result = self.model.pipeline(seg_list, tasks=["ner"])
        if len(result.ner) == 0:
            return final_augment_sentence
        for _ in range(self.augment_num):
            n, word = random.choice(result.ner)
            if n in self.combine_dict.keys():
                new_word = random.choice(list(self.combine_dict[n]))
                old_index = seg_list.index(word)
                seg_list[old_index] = new_word
                new_sentence = ''.join(seg_list)
                final_augment_sentence.append(new_sentence)

        return final_augment_sentence
