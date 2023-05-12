import random
from collections import defaultdict

from .base_func import BaseFunc


class AbbreviationFunc(BaseFunc):
    def __init__(self, config):
        super(AbbreviationFunc, self).__init__(config)
        self.augment_num = config.abbreviation_func.augment_num
        self.combine_dict = self.load_abbreviation_files()

    def load_abbreviation_files(self):
        combine_dict = defaultdict(set)

        for line in open("files/abbreviation/abbreviation.txt", "r", encoding="utf-8"):
            try:
                first, _, second = line.strip().split(',')
                combine_dict[first].add(second)
                self.add_word(first)
            except:
                continue

        return combine_dict

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)

        abbreviation_words = []
        for word in seg_list:
            if word in self.combine_dict:
                abbreviation_words.append(word)
        if len(abbreviation_words) == 0:
            return final_augment_sentence

        self.augment_num = min(self.augment_num, len(abbreviation_words))
        abbreviation_words = random.sample(abbreviation_words, self.augment_num)
        for change_word in abbreviation_words:
            new_words = seg_list.copy()
            word_idx = new_words.index(change_word)
            new_words[word_idx] = random.choice(list(self.combine_dict[change_word]))
            final_augment_sentence.append(''.join(new_words))

        return final_augment_sentence
