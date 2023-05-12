from zhconv import convert

from .base_func import BaseFunc


class SimplifiedTraditionalFunc(BaseFunc):
    def __init__(self, config):
        super(SimplifiedTraditionalFunc, self).__init__(config)

    def process(self, sentence):
        traditional = convert(sentence, "zh-hant")
        return [traditional]
