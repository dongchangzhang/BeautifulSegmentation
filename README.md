### somthings

* 应该可以在windows上运行，但是我没跑过
* 运行ui界面需要安装pyqt4，使用pip或者其他工具即可

### 目录结构

```
.
├── check.py # 检查工具， 现在没啥用 打算把验证代码放这
├── constant.py # 常量配置
├── model # 马尔科夫所需要的矩阵模型还有两个结巴分词类型的整理好的字典模型
│   ├── dict.big.json # 结巴字典 词语尽可能长的
│   ├── dict.small.json # 同上 词语较短
│   ├── dict.stop.json # 同上 停止词
│   ├── EmitProbMatrix2.json # 2阶马尔科夫发射矩阵
│   ├── EmitProbMatrix.json # 1阶
│   ├── hash.txt # 没啥用 md5
│   ├── InitStatus.json # 初始化字典
│   ├── letter_mark.txt # 将训练样本标注后的文本
│   ├── status.txt # 状态集合文本 BMMEBES之类的
│   ├── TransProbMatrix2.json # 状态转移矩阵2hmm
│   └── TransProbMatrix.json # 同上 1hmm
├── out # 文件分词的输出结果
│   └── judge.data.1.out.txt
├── __pycache__
│   ├── check.cpython-35.pyc
│   ├── config.cpython-35.pyc
│   ├── constant.cpython-35.pyc
│   ├── split.cpython-35.pyc
│   └── train.cpython-35.pyc
├── README.md
├── res # 资源文件
│   ├── ans
│   │   ├── judge.data.ans.1 # 两个训练答案
│   │   └── judge.data.ans.2
│   ├── dict # 词典
│   │   ├── dict.txt
│   │   ├── dict.txt.big
│   │   ├── dict.txt.small
│   │   ├── idf.txt.big
│   │   └── stop_words.txt
│   ├── icon.svg # 图标
│   ├── test # 测试集合
│   │   ├── judge.data.1
│   │   ├── judge.data.1.out.txt
│   │   └── judge.data.2
│   └── train # 训练集合
│       └── cip-data.train
├── run.py # 命令行下跑
├── split.py # 拆分 维特比
├── tmp # 用于ui界面的缓存文件
│   └── tmp.txt
├── train.py # 训练模型
└── ui.py # ui界面

```
### 其他
split.py 和train.py 中有一半代码是尝试2阶hmm和字典分词的代码（没写完不能用）只能用1阶hmm