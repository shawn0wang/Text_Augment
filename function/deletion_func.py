import random

from .base_func import BaseFunc


class DeletionFunc(BaseFunc):
    def __init__(self, config):
        super(DeletionFunc, self).__init__(config)
        self.augment_num = config.deletion_func.augment_num
        self.del_p = config.deletion_func.del_p

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)
        if len(seg_list) == 1:
            return final_augment_sentence

        for _ in range(self.augment_num):
            new_words = []
            for word in seg_list:
                r = random.uniform(0, 1)
                if r > self.del_p:
                    new_words.append(word)

            if len(new_words) == 0:
                rand_int = random.randint(0, len(seg_list) - 1)
                new_words = [seg_list[rand_int]]

            new_sentence = ''.join(new_words)
            final_augment_sentence.append(new_sentence)

        return final_augment_sentence
