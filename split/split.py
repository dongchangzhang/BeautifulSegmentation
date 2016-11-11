import os
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
        print(self.is_dic)

    def split_for_file(self, *files):
        for file in files:
            try:
                with open(file, "r") as f:
                    with open(OUT_DIR + file + ".out.txt", "w") as out:
                        for sentence in f:
                            out.write(self.split_for_sentence(sentence) + "\n")
            except:
                print("Not find file: " + file)

    def split_for_sentence(self, sentence):
        # to prepare

        sentence_len = len(sentence)
        weight = [[0] * sentence_len] * 4
        path = [[0] * sentence_len] * 4

        # init weight

        # sentence[0] as B
        weight[0][0] = self.is_dic["B"] + self.epm_dic[sentence[0]]["B"]
        # sentence[0] as M
        weight[0][1] = self.is_dic["M"] + self.epm_dic[sentence[0]]["M"]
        # sentence[0] as E
        weight[0][2] = self.is_dic["E"] + self.epm_dic[sentence[0]]["E"]
        # sentence[0] as S
        weight[0][3] = self.is_dic["S"] + self.epm_dic[sentence[0]]["S"]

        # calculate weight && path
        for i in range(1, sentence_len):
            for j in range(1, 4):
                weight[j][i] = MIN
                path[j][i] = -1
                for k in range(1, 4):
                    tmp = weight[k][i-1] + self.tpm_dic[k][j] + self.epm_dic[j][sentence[i]]
                    if tmp >weight[j][i]
                        weight[j][i] = tmp
                        path[j][i] = k
        # confirm back point
        if weight[2][sentence_len - 1] > weight[3][sentence_len - 1]:
            back_point = 2
        else:
            back_point = 3


        return ""

if __name__ == "__main__":
    test = Spliter()
    test.split_for_sentence("小明毕业于清华大学")
