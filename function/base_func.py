from abc import ABCMeta, abstractmethod

import jieba
import torch
from ltp import LTP

from function import stop_words_list


class BaseFunc(metaclass=ABCMeta):
    def __init__(self, config, extra_file=None):
        self.config = config

        # choose cut words tool
        if config.cut_words_tool_name == "jieba":
            self.cut_words_tool = jieba
        else:
            self.cut_words_tool = LTP(config.cut_words_tool_name)
            if torch.cuda.is_available():
                self.cut_words_tool.to("cuda")

        if extra_file:
            self.combine_dict = self.load_extra_file(extra_file)
        else:
            self.combine_dict = None

        self.stop_words_list = [stop_word[:-1] for stop_word in open(stop_words_list[config.stop_words]).readlines()]

    def cut_words(self, sentence):
        if self.config.cut_words_tool_name == "jieba":
            seg_list = list(self.cut_words_tool.cut(sentence))
        else:
            seg_list = self.cut_words_tool.pipeline([sentence], tasks=["cws"]).cws[0]

        return seg_list

    def add_word(self, word):
        self.cut_words_tool.add_word(word)

    def load_extra_file(self, extra_file):
        combine_dict = {}
        for line in open(extra_file, "r", encoding="utf-8"):
            seg_list = line.strip().split(" ")
            for i in range(len(seg_list)):
                wi = seg_list[i]
                # add to user dict
                if len(wi) > 1:
                    self.add_word(wi)
                combine_dict[wi] = list(set(seg_list) - {wi})
        return combine_dict

    @abstractmethod
    def process(self, sentence):
        pass
