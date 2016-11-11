import os
import platform

# location of here
HERE = os.getcwd()
# parent node location
loc = HERE.rfind('/') + 1
# the project location
LAST_DIR = HERE[0:loc]
# train data answer location
ANS_LOCATION = LAST_DIR + "res/ans/"
# dict location
DICT_LOCATION = LAST_DIR + "res/dict/"
# test data location
TEST_LOCATION = LAST_DIR + "res/test/"





# os type
MY_OS = platform.system()
# os information
OS_INFO = platform.platform()

if __name__ == "__main__":
    print(MY_OS)
