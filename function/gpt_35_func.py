import warnings

import openai

from .base_func import BaseFunc


class Gpt35Func(BaseFunc):
    def __init__(self, config):
        super(Gpt35Func, self).__init__(config)
        self.augment_num = config.augment_num
        self.api_key = config.api_key

    def process(self, sentence):
        if self.augment_num > 10:
            warnings.warn("不建议一次性生成增强数据超过10个，会影响生成质量")

        final_augment_sentence = []
        conversation = [
            {
                "role": "system",
                "content": "你是一个有用的助手"
            },
            {
                "role": "user",
                "content": f"请把'{sentence}'，在相同意思的前提下，换{self.augment_num}种不同的表达方式"
            }]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=1,
            max_tokens=1024,
            top_p=0.9
        )
        result = [response["choices"][0]["message"]["content"]]
        for idx, item in enumerate(result[0].split("\n")[:-1]):
            final_augment_sentence.append(item.split(f"{idx + 1}.")[1])

        return final_augment_sentence
