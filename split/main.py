import sys
sys.path.append("..")

from config.config import *
from check.check import check_model
from model.train import start_train

if __name__ == "__main__":
    # start
    print("STARTING, PLEASE WAIT...")
    # judge
    status = check_model(LAST_DIR + "/model/")
    print(status)
    if status != 0:
        start_train()
    # done
    print("ALL DONE!")

    # input
    while True:
        sentence = input()
        print(sentence)
        if sentence == "exit":
            break
    # split && output

    # check result


