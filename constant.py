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

# sample
# train data location
TRAIN_SOURCE = os.path.join(RESOURCE_DIR, RES_TRAIN, 'cip-data.train')
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

# hmm2
# save TransProbMatrix in there
TPM_JSON2 = os.path.join(MODEL_DIR, 'TransProbMatrix2.json')
# save EmitProbMatrix  in there
EPM_JSON2 = os.path.join(MODEL_DIR, 'EmitProbMatrix2.json')


# dict
# dict big source
DICT_BIG_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.big')
# save dict big
DICT_BIG_JSON = os.path.join(MODEL_DIR, 'dict.big.json')
# dict small
DICT_SMALL_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'dict.txt.small')
# save dict small
DICT_SMALL_JSON = os.path.join(MODEL_DIR, 'dict.small.json')
# dict stop source
DICT_STOP_SOURCE = os.path.join(RESOURCE_DIR, RES_DICT, 'stop_words.txt')
# save stop big
DICT_STOP_JSON = os.path.join(MODEL_DIR, 'dict.stop.json')

# tmp
TMP_FILE = os.path.join('tmp', 'tmp.txt')
# model hash if model change we need retrain
HASH_VALUE = os.path.join(MODEL_DIR, 'hash.txt')



