import os
import platform

# location of here
HERE = os.getcwd()

# os type
MY_OS = platform.system()
# os information
OS_INFO = platform.platform()

if __name__ == "__main__":
    print(MY_OS)
