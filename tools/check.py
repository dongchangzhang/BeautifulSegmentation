import os
import hashlib


HERE = os.path.split(os.path.realpath(__file__))[0]
# last dir
LAST_DIR = HERE[0:HERE.rfind("/")]
# model hash if model change we need retrain
HASH_VALUE = LAST_DIR + "/" + "model/hash.txt"
# train data location
TRAIN_SOURCE = LAST_DIR + "/" + "res/train/cip-data.train"


def check_model():
    print("Start checking model...")
    cm = ModelDiff(LAST_DIR + "/model/")
    return cm.status


class ModelDiff:
    def __init__(self, location):
        self.location = location
        self.list_dir = os.listdir(location)
        self.list_dir = [location + x for x in self.list_dir]
        self.list_dir.append(TRAIN_SOURCE)
        self.list_dir.sort(key=lambda item: item[1], reverse=True)
        self.hash = ""
        self.status = 0
        self.do_check()

    def get_md5(self, silence=True):
        md5_tool = hashlib.md5()
        for file in self.list_dir:
            if not file.endswith("_") and file != HASH_VALUE:
                if not silence:
                    print("hashing: " + file)
                with open(file, "r", encoding='utf-8') as f:
                    while True:
                        b = f.read(8096)
                        if not b:
                            break
                        md5_tool.update(b.encode("utf8"))
        self.hash = md5_tool.hexdigest()

    def write_hash(self):
        with open(HASH_VALUE, "w") as f:
            f.write(self.hash)

    def do_check(self):
        try:
            self.get_md5(True)
            with open(HASH_VALUE, "r") as f:
                md5 = f.readline()
            if self.hash == md5:
                self.status = 0
                print("Success!")
            else:
                print("model changed, need retrain")
                self.status = -1
                self.get_md5()
                self.write_hash()

        except IOError:
            print("files not be hashed...")
            self.get_md5()
            self.write_hash()

    def status(self):
        return self.status


if __name__ == "__main__":
    test = ModelDiff(LAST_DIR + "/model/")
    test.do_check()
