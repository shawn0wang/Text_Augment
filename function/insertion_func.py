import random

from .base_func import BaseFunc


class InsertionFunc(BaseFunc):
    def __init__(self, config):
        super(InsertionFunc, self).__init__(config)
        self.augment_num = config.insertion_func.augment_num
        self.change_num = config.insertion_func.change_num

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)

        for _ in range(self.augment_num):
            new_words = seg_list.copy()
            for _ in range(self.change_num):
                random_word = new_words[random.randint(0, len(new_words) - 1)]
                random_idx = random.randint(0, len(new_words) - 1)
                new_words.insert(random_idx, random_word)
            new_sentence = ''.join(new_words)
            final_augment_sentence.append(new_sentence)

        return final_augment_sentence
