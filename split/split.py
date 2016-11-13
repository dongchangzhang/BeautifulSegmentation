import os
import re
import json

# here
HERE = os.path.split(os.path.realpath(__file__))[0]
# parent
LAST_DIR = HERE[0:HERE.rfind("/")]
# file output
OUT_DIR = LAST_DIR + "/out/"
# save InitStatus location in there
IS_JSON = LAST_DIR + "/model/InitStatus.json"
# save TransProbMatrix location in there
TPM_JSON = LAST_DIR + "/model/TransProbMatrix.json"
# save EmitProbMatrix location in there
EPM_JSON = LAST_DIR + "/model/EmitProbMatrix.json"

MIN = -3.14e+100


def split_file(*files):
    spliter = Spliter()
    spliter.split_for_file(files)


def split_sentence(sentence):
    spliter = Spliter()
    return spliter.split_for_sentence(sentence)

class Spliter:
    def __init__(self):
        self.is_dic = {}
        self.tpm_dic = {}
        self.epm_dic = {}
        with open(IS_JSON, "r") as f:
            self.is_dic = json.load(f)
        with open(TPM_JSON, "r") as f:
            self.tpm_dic = json.load(f)
        with open(EPM_JSON, "r") as f:
            self.epm_dic = json.load(f)

    def split_for_file(self, *files):
        for file in files:
            try:
                with open(file, "r") as f:
                    with open(OUT_DIR + file[file.rfind("/"):] + ".out.txt", "w") as out:
                        for sentence in f:
                            out.write(self.split_for_sentence(sentence) + "\n")
            except:
                print("Not find file: " + file)

    def split_for_sentence(self, sentence):
        # to prepare
        mark = {0: "B", 1: "M", 2: "E", 3: "S"}
        sentence_len = len(sentence)
        weight = [([MIN] * sentence_len) for i in range(0, 4)]
        path = [([-1] * sentence_len) for i in range(0, 4)]

        # init weight
        if sentence[0] not in self.epm_dic:
            value = {
                "B": self.epm_dic["NONE"],
                "M": MIN,
                "E": MIN,
                "S": self.epm_dic["NONE"],}
        else:
            value = {
                "B": self.epm_dic[sentence[0]]["B"],
                "M": self.epm_dic[sentence[0]]["M"],
                "E": self.epm_dic[sentence[0]]["E"],
                "S": self.epm_dic[sentence[0]]["S"]
            }
        # sentence[0] as B
        weight[0][0] = self.is_dic["B"] + value["B"]
        # sentence[0] as M
        weight[1][0] = self.is_dic["M"] + value["M"]
        # sentence[0] as E
        weight[2][0] = self.is_dic["E"] + value["E"]
        # sentence[0] as S
        weight[3][0] = self.is_dic["S"] + value["S"]

        # calculate weight && path
        for i in range(1, sentence_len):
            for j in range(0, 4):
                weight[j][i] = MIN
                path[j][i] = -1
                for k in range(0, 4):
                    if sentence[i] not in self.epm_dic:
                        tmp = weight[k][i - 1] + self.tpm_dic[mark[k]][mark[j]] + self.epm_dic["NONE"]
                    else:
                        tmp = weight[k][i-1] + self.tpm_dic[mark[k]][mark[j]] + self.epm_dic[sentence[i]][mark[j]]
                    if tmp > weight[j][i]:
                        weight[j][i] = tmp
                        path[j][i] = k

        # confirm back point

        if weight[2][sentence_len - 1] > weight[3][sentence_len - 1]:
            back_point = 2
        else:
            back_point = 3

        rmark_result = ""
        # print(weight[0])
        # print(weight[1])
        # print(weight[2])
        # print(weight[3])
        #
        # print(path[0])
        # print(path[1])
        # print(path[2])
        # print(path[3])
        # back up
        for i in range(0, sentence_len - 1):

            rmark_result += mark[back_point]
            back_point = path[back_point][sentence_len - 1 - i]
        rmark_result += mark[back_point]
        mark_result = rmark_result[::-1]

        return self.get_result(sentence, mark_result)

    def get_result(self, sentence, mark):
        word_list = []
        start = 0
        for i in range(0, len(mark)):
            if mark[i] == "S":
                word_list.append(sentence[i])
            elif mark[i] == "B":
                start = i
            elif mark[i] == "E":
                end = i + 1
                word_list.append(sentence[start:end])

        format_list = []
        tmp = ""
        for word in word_list:

            r = re.match(r"([0-9a-zA-Z:/\\@#$%.*])*", word)
            if r.group(0) == word:
                tmp += word
            else:
                if tmp != "":
                    format_list.append(tmp)
                    format_list.append(word)
                    tmp = ""
                else:
                    format_list.append(word)
        if tmp != "":
            format_list.append(tmp)

        return "\t".join(format_list)

if __name__ == "__main__":
    test = Spliter()
    test.split_for_sentence("张东昌拔出宝剑")
    test.split_for_file("../res/test/judge.data.1")
