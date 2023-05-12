stop_words_list = {
    "baidu": "files/stopwords/baidu_stopwords.txt",
    "cn": "files/stopwords/cn_stopwords.txt",
    "hit": "files/stopwords/hit_stopwords.txt",
    "scu": "files/stopwords/scu_stopwords.txt"
}

seq2seq_model_config = {
    "simbert_tiny": {
        "model_dir": "chinese_simbert_L-4_H-312_A-12",
        "download_url": "https://open.zhuiyi.ai/releases/nlp/models/zhuiyi/chinese_simbert_L-4_H-312_A-12.zip"
    },
    "simbert_small": {
        "model_dir": "chinese_simbert_L-6_H-384_A-12",
        "download_url": "https://open.zhuiyi.ai/releases/nlp/models/zhuiyi/chinese_simbert_L-6_H-384_A-12.zip"
    },
    "simbert_base": {
        "model_dir": "chinese_simbert_L-12_H-768_A-12",
        "download_url": "https://open.zhuiyi.ai/releases/nlp/models/zhuiyi/chinese_simbert_L-12_H-768_A-12.zip"
    },
    "roformer_sim_small": {
        "model_dir": "chinese_roformer-sim-char-ft_L-6_H-384_A-6",
        "download_url": "https://open.zhuiyi.ai/releases/nlp/models/zhuiyi/chinese_roformer-sim-char-ft_L-6_H-384_A-6.zip"
    },
    "roformer_sim_base": {
        "model_dir": "chinese_roformer-sim-char-ft_L-12_H-768_A-12",
        "download_url": "https://open.zhuiyi.ai/releases/nlp/models/zhuiyi/chinese_roformer-sim-char-ft_L-12_H-768_A-12.zip"
    }
}
