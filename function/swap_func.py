import random

from .base_func import BaseFunc


class SwapFunc(BaseFunc):
    def __init__(self, config, extra_file=None):
        super(SwapFunc, self).__init__(config, extra_file)
        self.augment_num = config.swap_func.augment_num
        self.change_num = config.swap_func.change_num

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)

        for _ in range(self.augment_num):
            new_words = seg_list.copy()
            for _ in range(self.change_num):
                random_idx_1 = random.randint(0, len(new_words) - 1)
                random_idx_2 = random.randint(0, len(new_words) - 1)
                counter = 0
                while random_idx_1 == random_idx_2:
                    random_idx_2 = random.randint(0, len(new_words) - 1)
                    counter += 1
                    if counter > 3:
                        break
                new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
            new_sentence = ''.join(new_words)
            final_augment_sentence.append(new_sentence)

        return final_augment_sentence
