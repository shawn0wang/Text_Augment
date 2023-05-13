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
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"请把'{sentence.strip()}'，在不改变意思的前提下，换{self.augment_num}种不同的表达方式，并以'结果：'开头返回结果",
                temperature=1,
                max_tokens=500,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            result = [response["choices"][0]["text"].split("结果：")[1].strip()]
            for idx, item in enumerate(result[0].split("\n")):
                final_augment_sentence.append(item.split(f"{idx + 1}.")[1])
        except:
            return final_augment_sentence

        return final_augment_sentence
