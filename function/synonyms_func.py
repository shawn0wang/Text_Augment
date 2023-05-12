import random

import synonyms

from .base_func import BaseFunc


class SynonymsFunc(BaseFunc):
    def __init__(self, config, extra_file=None):
        super(SynonymsFunc, self).__init__(config, extra_file)
        self.augment_num = config.synonyms_func.augment_num
        self.change_num = config.synonyms_func.change_num
        self.size = config.synonyms_func.size
        self.threshold = config.synonyms_func.threshold

    @staticmethod
    def get_synonyms(word, size=10, threshold=0.5):
        words, scores = synonyms.nearby(word, size)
        synonyms_words = [word for word, score in zip(words, scores) if score >= threshold]
        return synonyms_words[1:]

    def process(self, sentence):
        final_augment_sentence = []
        seg_list = self.cut_words(sentence)
        random_word_list = list(set([word for word in seg_list if word not in self.stop_words_list]))

        for _ in range(self.augment_num):
            random.shuffle(random_word_list)
            num_replaced = 0
            new_words = seg_list.copy()
            for random_word in random_word_list:
                if self.combine_dict:
                    new_words = [random.choice(self.combine_dict[word])
                                 if word == random_word and word in self.combine_dict else word for word in new_words]
                else:
                    synonyms_words = self.get_synonyms(random_word, self.size, self.threshold)
                    if len(synonyms_words) > 1:
                        synonym = random.choice(synonyms_words)
                        new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
                if num_replaced >= self.change_num:
                    break
            new_sentence = ''.join(new_words)
            final_augment_sentence.append(new_sentence)

        return final_augment_sentence
