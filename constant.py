import os
import platform

# prepare
# get the platform of the system
SYSTEM = platform.system()
# linux type
LINUX = 'Linux'
# macosx type
MACOSX = 'Darwin'
# windows type
WINDOWS = 'Windows'
# directory separator
PATHSEP = os.path.sep
# hmm model and words dict will be saved in there
MODEL_DIR = 'model'
# file output in there
OUT_DIR = os.path.join('out', '')
# resource dir
RESOURCE_DIR = 'res'
# tran data dir
RES_TRAIN = 'train'
# dict dir
RES_DICT = 'dict'

# probability
# one thing can not happened
MIN = -3.14e+100

# the max match length for longest in long mode
MAX_LEN_L = 8
# the max match length for longest in short mode
MAX_LEN_S = 4 

# sample
# train data location
TRAIN_SOURCE = os.path.join(RESOURCE_DIR, RES_TRAIN, 'cip-data.train')
TRAIN_SOURCES = os.path.join(RESOURCE_DIR, RES_TRAIN)
# mark train data and save in there
AFTER_MARK = os.path.join(MODEL_DIR, 'letter_mark.txt')
# all status char will be put in this file by order
STATUS_FILE = os.path.join(MODEL_DIR, 'status.txt')

# hmm1
# save InitStatus in there
IS_JSON = os.path.join(MODEL_DIR, 'InitStatus.json')
# save TransProbMatrix location in there
TPM_JSON = os.path.join(MODEL_DIR, 'TransProbMatrix.json')
# save EmitProbMatrix location in there
EPM_JSON = os.path.join(MODEL_DIR, 'EmitProbMatrix.json')


# dict
# dict big source
DICT_BIG_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.big')
# dict small
DICT_SMALL_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.small')
# dict other source
DICT_OTHER_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.other')
# dict other source
DICT_IDF_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.idf')
# save
DICT_BIG_JSON = os.path.join(MODEL_DIR, 'dict.big.json')
DICT_SMALL_JSON = os.path.join(MODEL_DIR, 'dict.small.json')
DICT_TEST_JSON = os.path.join(MODEL_DIR, 'dict.test.json')

# tmp
TMP_FILE = os.path.join('tmp', 'tmp.txt')
# model hash if model change we need retrain
HASH_VALUE = os.path.join(MODEL_DIR, 'hash.txt')
# icons
ICONS = os.path.join(RESOURCE_DIR, 'icon.svg')

# test files
FOR_TEST1= os.path.join(RESOURCE_DIR, 'test', 'judge.data.1')
FOR_TEST2= os.path.join(RESOURCE_DIR, 'test', 'judge.data.2')

# test ans
TEST1= os.path.join(RESOURCE_DIR, 'ans', 'judge.data.ans.1')
TEST2= os.path.join(RESOURCE_DIR, 'ans', 'judge.data.ans.2')

# result
JUDGE1= os.path.join('out', 'judge.data.1.out.txt')
JUDGE2= os.path.join('out', 'judge.data.2.out.txt')




