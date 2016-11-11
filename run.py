from model.train import start_train
from tools.check import check_model


class BeautifulSegmentation:

    def __init__(self):
        self.do_init()

    def do_init(self):
        print("Starting Work...")
        status = check_model()
        if status == -1:
            start_train()

    def arg_parser(self):
        pass

    def do_file(self):
        pass

    def do_sentence(self):
        pass






