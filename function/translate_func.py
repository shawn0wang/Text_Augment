import hashlib
import random

import requests
from googletrans import Translator

from .base_func import BaseFunc


class TranslateFunc(BaseFunc):
    def __init__(self, config):
        super(TranslateFunc, self).__init__(config)
        self.augment_num = config.translate_func.augment_num
        self.trans_tool = config.translate_func.trans_tool
        if self.trans_tool == "baidu":
            self.app_id = config.translate_func.app_id
            self.secret_key = config.translate_func.secret_key
        elif self.trans_tool == "google":
            self.translator = Translator()

    def _google_trans(self, sentence, t_from, t_to):
        translations = self.translator.translate(sentence, dest=t_to, src=t_from)
        return translations.text

    def _baidu_trans(self, sentence, t_from, t_to):
        if len(sentence) > 4891:
            raise ValueError("输入请不要超过4891个字符！")

        salt = str(random.randint(0, 50))
        sign = self.app_id + sentence + salt + self.secret_key
        sign = hashlib.md5(sign.encode(encoding="UTF-8")).hexdigest()
        head = {
            "q": f"{sentence}",
            "from": f"{t_from}",
            "to": f"{t_to}",
            "appid": f"{self.app_id}",
            "salt": f"{salt}",
            "sign": f"{sign}"}
        response = requests.get("http://api.fanyi.baidu.com/api/trans/vip/translate", head)
        res = response.json()["trans_result"][0]["dst"]
        return res

    def process(self, sentence):
        final_augment_sentence = []

        for _ in range(self.augment_num):
            if self.trans_tool == "baidu":
                en_sentence = self._baidu_trans(sentence, t_from="zh", t_to="en")
                sentence = self._baidu_trans(en_sentence, t_from="en", t_to="zh")
                final_augment_sentence.append(sentence)
            else:
                en_sentence = self._google_trans(sentence, t_from="zh-cn", t_to="en")
                sentence = self._google_trans(en_sentence, t_from="en", t_to="zh-cn")
                final_augment_sentence.append(sentence)

        return final_augment_sentence
