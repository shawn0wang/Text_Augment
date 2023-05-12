import os
import sys
import zipfile

import numpy as np
import wget
from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.snippets import sequence_padding, AutoRegressiveDecoder
from bert4keras.tokenizers import Tokenizer

from function import seq2seq_model_config
from .base_func import BaseFunc


class Seq2SeqSimFunc(BaseFunc, AutoRegressiveDecoder):
    def __init__(self, config):
        BaseFunc.__init__(self, config)
        self.augment_num = config.seq2seq_sim_func.augment_num

        # 检查模型是否已下载，没有则下载相关模型
        model_name = config.seq2seq_sim_func.model
        model_config = seq2seq_model_config[model_name]
        model_path = os.path.join("model", model_config["model_dir"])
        if not os.path.exists(model_path):
            wget.download(model_config["download_url"], out=f"{model_path}.zip", bar=self.bar_progress)
            with zipfile.ZipFile(f"{model_path}.zip", "r") as zip_ref:
                zip_ref.extractall(path="model")

        # 将相关配置进行加载
        self.bert_config_path = os.path.join(model_path, "bert_config.json")
        self.checkpoint_path = os.path.join(model_path, "bert_model.ckpt")
        self.dict_path = os.path.join(model_path, "vocab.txt")
        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)
        self.bert = build_transformer_model(
            self.bert_config_path,
            self.checkpoint_path,
            with_pool='linear',
            application='unilm',
            return_keras_model=False)
        self.encoder = keras.models.Model(self.bert.model.inputs, self.bert.model.outputs[0])
        self.seq2seq = keras.models.Model(self.bert.model.inputs, self.bert.model.outputs[1])
        self.max_len = 512
        self.start_id = None
        self.end_id = self.tokenizer._token_end_id
        AutoRegressiveDecoder.__init__(self, self.start_id, self.end_id, self.max_len)

    @staticmethod
    def bar_progress(current, total, width=80):
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    @AutoRegressiveDecoder.set_rtype('probas')
    def predict(self, inputs, output_ids, step):
        token_ids, segment_ids = inputs
        token_ids = np.concatenate([token_ids, output_ids], 1)
        segment_ids = np.concatenate(
            [segment_ids, np.ones_like(output_ids)], 1)
        return self.seq2seq.predict([token_ids, segment_ids])[:, -1]

    def generate(self, text, n=1):
        token_ids, segment_ids = self.tokenizer.encode(text, max_length=self.max_len)
        output_ids = self.random_sample([token_ids, segment_ids], n, 5)  # 基于随机采样
        return [self.tokenizer.decode(ids) for ids in output_ids]

    def process(self, sentence):
        n = self.augment_num * 4
        r = self.generate(sentence, n=n)
        r = [i for i in set(r) if i != sentence]
        r = [sentence] + r
        X, S = [], []
        for t in r:
            x, s = self.tokenizer.encode(t)
            X.append(x)
            S.append(s)
        X = sequence_padding(X)
        S = sequence_padding(S)
        Z = self.encoder.predict([X, S])
        Z /= (Z ** 2).sum(axis=1, keepdims=True) ** 0.5
        argsort = np.dot(Z[1:], -Z[0]).argsort()
        return [r[i + 1] for i in argsort[:self.augment_num]]
