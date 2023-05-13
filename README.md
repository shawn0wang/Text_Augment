# TextAugment
TextAugment 是一个文本数据增强库，主要是为了方便数据增强工作，进行简单配置后即可通过不同的方法生成多种增强数据，
本库总结融合了多种数据增强方法，例如 EDA、SimBert、chatGPT等

## 数据增强方法介绍
本库目前包含了12种数据增强方法
### 1、简称替换——AbbreviationFunc
若文本中有一些词语具有简称，则可以将该词语替换为简称
> 例子：
> 
> 原文本：你知道外事管理办公室怎么走吗
> 
> 新文本：你知道外管办怎么走吗
### 2、反义词替换——AntonymFunc
将文本中的一些词替换为它的反义词
> 例子：
> 
> 原文本：外边的人还在过着饥寒交迫的生活
> 
> 新文本：外边的人还在过着纸醉金迷的生活
### 3、随机删除——DeletionFunc
将文本的词按照一定的概率进行删除
> 例子：
> 
> 原文本：今天晚上的天气怎么样
> 
> 新文本：今天的天气怎么样
### 4、GPT3 接口调用——Gpt3Func
### 5、ChatGPT 接口调用——Gpt35Func
调用 OpenAI 的 GPT3 或 ChatGPT 接口，来获取一些增强的数据
> 例子：
> 
> 原文本：今天晚上的天气怎么样（注：要求 GPT 返回意思相同的两句话）
> 
> 新文本1：今晚天气如何
> 
> 新文本2：今晚天气情况怎样
### 6、随机插入——InsertionFunc
随机将文本中的一些词语重复插入
> 例子：
> 
> 原文本：今天晚上的天气怎么样
> 
> 新文本：今天天气晚上的天气怎么样
### 7、实体替换——NerFunc
随机将文本中的实体替换为另一个实体
> 例子：
> 
> 原文本：你觉得这辆劳斯莱斯怎么样
> 
> 新文本：你觉得这辆奔驰怎么样
### 8、基于 SimBert 等模型的生成——Seq2SeqSimFunc
使用 SimBert 或 RoFormer-Sim 模型生成同义语句
> 例子：
> 
> 原文本：微信和支付宝哪个好
> 
> 新文本：支付宝和微信哪个好啊
### 9、简体转繁体——SimplifiedTraditionalFunc
将简体中文转化为繁体字
> 例子：
> 
> 原文本：微信和支付宝哪个好
> 
> 新文本：微信和支付寶哪個好
### 10、随机交换——SwapFunc
随机对文本中的词两两交换
> 例子：
> 
> 原文本：你觉得这辆劳斯莱斯怎么样
> 
> 新文本：你觉得怎么样劳斯莱斯这辆
### 11、同义词替换——SynonymsFunc
基于 synonyms 同义词库或使用你自己的同义词表，将文本中的某些词替换为相同意思的词
> 例子：
> 
> 原文本：今天的天气真好啊
> 
> 新文本：今天的天气真不错啊
### 12、回译——TranslateFunc
基于 Baidu 或 Google API，对文本进行中英文回译
> 例子：
> 
> 原文本：今天的天气真好啊
> 
> 新文本：今天天气真好

## 安装环境
使用 conda 创建新的环境: conda create -n 环境名 python==3.7.11

⚠️—— python 版本为3.7.11

## 使用
#### 1. 使用 `git clone` 或下载文件的方式将库下载到本地，随后进入项目根目录使用 `pip install -r requeirments.txt`命令安装项目所需环境
#### 2. 查看根目录下 `config.yaml`，进行个性化配置设置
#### 3. 将你需要增强的数据文件放在 `data_loader/data` 目录下
#### 4. 查看 `data_loader` 目录下的 `demo.py` 文件
TextDataAugment 不会限制你的数据处理过程，你需要创建自己的 data_loader 进行数据处理，
把你的 data_loader 放到 `data_loader/data` 目录下，例如`demo_data_loader.py` 
```python
import json
import os
from typing import List

from .base_loader import Data, DataLoader


class DemoDataLoader(DataLoader):
    def __init__(self, data_name, save_file_name):
        super(DemoDataLoader, self).__init__(save_file_name)
        self.data_name = data_name
        self.data_path = os.path.join(self.data_dir, data_name)

    def read_data(self) -> List[Data]:
        all_data = []
        with open(self.data_path, "r", encoding="UTF-8") as f:
            for idx, data in enumerate(f.readlines()):
                json_data = json.loads(data)
                sentence = json_data["sentence"]
                all_data.append(
                    Data(data_id=str(idx), sentence=sentence, from_file=self.data_name)
                )
        return all_data
```
每个 data_loader 必须继承 `DataLoader` 类，并重写 `DataLoader` 中的 `read_data` 方法，你可以自定义参数，
以及在 `read_data` 方法编写你的数据处理逻辑


在 dataloader 的`__init__` 中 `save_file_name` 参数是必须被提供的，用来存储增强的数据，增强后的数据最终会被存放在
`data_loader/augment_data` 目录下，例如 `demo_augment.jsonl`


`read_data` 方法最终必须返回一个 `List[Data]`，`Data`类主要是为了规整数据，并方便你快速对应原数据/文件，其类如下：
```python
class Data:
    def __init__(self, data_id: str, sentence: str, from_file: str):
        self.data_id = self._check_valid(data_id, str)
        self.sentence = self._check_valid(sentence, str)
        self.from_file = self._check_valid(from_file, str)

    @staticmethod
    def _check_valid(value, type_name):
        if not isinstance(value, type_name):
            raise TypeError(f"{value} must be a {type_name}")
        else:
            return value
```
现在开始编写你自己的数据处理 `loader` 吧
#### 5. 在 `data_loader/__init__.py` 文件中将你的 `data_loader`，添加到 `run_loader` 列表中
#### 6. 运行 `main.py` 等待结果即可

### QA
Q：使用苹果M系列芯片运行 Seq2SeqSimFunc 时出现：Process finished with exit code 132 (interrupted by signal 4: SIGILL)

A：卸载 tensorflow 后使用 conda 进行安装，conda install tensorflow==1.14.0


