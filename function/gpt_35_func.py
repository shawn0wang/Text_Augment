import warnings

import openai

from .base_func import BaseFunc


class Gpt35Func(BaseFunc):
    def __init__(self, config):
        super(Gpt35Func, self).__init__(config)
        self.augment_num = config.gpt_35_func.augment_num
        openai.api_key = config.gpt_35_func.api_key

    def process(self, sentence):
        if self.augment_num > 10:
            warnings.warn("不建议一次性生成增强数据超过10个，会影响生成质量")

        final_augment_sentence = []
        try:
            conversation = [
                {
                    "role": "system",
                    "content": "你是一个有用的助手"
                },
                {
                    "role": "user",
                    "content": f"请把'{sentence.strip()}'，在不改变意思的前提下，换{self.augment_num}种不同的表达方式，并以'结果：'开头返回结果"
                }]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=1,
                max_tokens=1024,
                top_p=0.9
            )
            result = [response["choices"][0]["message"]["content"].split("结果：")[1].strip()]
            for idx, item in enumerate(result[0].split("\n")):
                final_augment_sentence.append(item.split(f"{idx + 1}.")[1])
        except:
            return final_augment_sentence

        return final_augment_sentence
