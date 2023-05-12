import warnings

import openai

from .base_func import BaseFunc


class Gpt3Func(BaseFunc):
    def __init__(self, config):
        super(Gpt3Func, self).__init__(config)
        self.augment_num = config.gpt_3_func.augment_num
        openai.api_key = config.gpt_3_func.api_key

    def process(self, sentence):
        if self.augment_num > 5:
            warnings.warn("不建议一次性生成增强数据超过5个，会影响生成质量")

        final_augment_sentence = []
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"请把'{sentence}'，在相同意思的前提下，换{self.augment_num}种不同的表达方式",
            temperature=1,
            max_tokens=500,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        result = [response["choices"][0]["text"]]
        print(result)
        for idx, item in enumerate(result[0].split("\n")[:-1]):
            final_augment_sentence.append(item.split(f"{idx + 1}.")[1])

        return final_augment_sentence
