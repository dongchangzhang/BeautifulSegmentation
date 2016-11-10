import os
import platform

# location of here
here = os.getcwd()
# parent node location
loc = here.rfind('/') + 1
# the project location
ROOT = here[0:loc]
# train data answer location
ANS_LOCATION = ROOT + "res/ans/"
# dict location
DICT_LOCATION = ROOT + "res/dict/"
# test data location
TEST_LOCATION = ROOT + "res/test/"
# train data location
TRAIN_LOCATION = ROOT + "res/train/cip-data.train"

# os type
MY_OS = platform.system()
# os information
OS_INFO = platform.platform()

if __name__ == "__main__":
    print(MY_OS)
