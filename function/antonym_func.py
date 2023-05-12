import random
from collections import defaultdict

from .base_func import BaseFunc


class AntonymFunc(BaseFunc):
    def __init__(self, config):
        super(AntonymFunc, self).__init__(config)
        self.augment_num = config.antonym_func.augment_num
        self.combine_dict = self.load_antonym_files()

    @staticmethod
    def load_antonym_files():
        combine_dict = defaultdict(set)

        for line in open("files/antonym/antonym.txt", "r", encoding="utf-8"):
            first, second = line.strip().split('@')
            combine_dict[first].add(second)
            combine_dict[second].add(first)

        return combine_dict

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)

        antonym_words = []
        for word in seg_list:
            if word in self.combine_dict:
                antonym_words.append(word)
        if len(antonym_words) == 0:
            return final_augment_sentence

        self.augment_num = min(self.augment_num, len(antonym_words))
        antonym_words = random.sample(antonym_words, self.augment_num)
        for change_word in antonym_words:
            new_words = seg_list.copy()
            word_idx = new_words.index(change_word)
            new_words[word_idx] = random.choice(list(self.combine_dict[change_word]))
            final_augment_sentence.append(''.join(new_words))

        return final_augment_sentence
