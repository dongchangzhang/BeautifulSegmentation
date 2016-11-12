from model.train import start_train
from tools.check import check_model
from split.split import split_file
from split.split import split_sentence


class BeautifulSegmentation:

    def __init__(self):
        self.do_init()
        self.do_sentence()

    def do_init(self):
        print("Starting Work...")
        status = check_model()
        if status == -1:
            print("haha")
            start_train()
            check_model()


    def arg_parser(self):
        pass

    def do_file(self, *file):
        split_file(file)

    def do_sentence(self):
        while True:
            sentence = input("input sentence: ")
            print(split_sentence(sentence))

if __name__ == "__main__":
    r = BeautifulSegmentation()






