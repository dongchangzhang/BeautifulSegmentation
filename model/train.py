#!/usr/bin/env python3
import os
import json
import math
import codecs


MIN = -3.14e+100
# marked file : XBXMXMXE ....
AFTER_MARK = "letter_mark.txt"
# all status char will be put in this file by order
STATUS_FILE = "status.txt"
# save InitStatus location in there
IS_JSON = "InitStatus.json"
# save TransProbMatrix location in there
TPM_JSON = "TransProbMatrix.json"
# save EmitProbMatrix location in there
EPM_JSON = "EmitProbMatrix.json"
# train data location
TRAIN_SOURCE = "res/train/cip-data.train"


def start_train():
    here = os.path.split(os.path.realpath(__file__))[0]
    after_mark = here + "/" + AFTER_MARK
    status_file = here + "/" + STATUS_FILE
    is_json = here + "/" + IS_JSON
    tpm_json = here + "/" + TPM_JSON
    epm_json = here + "/" + EPM_JSON
    train_source = here[0:here.rfind("/")] + "/" + TRAIN_SOURCE
    Train(train_source, after_mark, status_file, is_json, tpm_json, epm_json)


class Train:
    def __init__(self, train_source, after_mark, status_file, is_json, tpm_json, epm_json):
        self.train_source = train_source
        self.after_mark = after_mark
        self.status_file = status_file
        self.is_json = is_json
        self.tpm_json = tpm_json
        self.epm_json = epm_json

        self.mark = MarkSample(self.train_source, self.after_mark, self.status_file)
        self.mark.train()
        self.statistics = Statistics(self.after_mark, self.status_file, self.epm_json, self.tpm_json, self.is_json)
        self.statistics.run()


class MarkSample:
    def __init__(self,
                 train_file, after_mark, status_file):
        self.f = open(train_file, "r")
        self.of = open(after_mark, "w")
        self.of2 = open(status_file, "w")

    def train(self):

        for line in self.f:
            self.deal_sentence(line)

        self.close()

    def deal_sentence(self, sentence):

        wlist = sentence.split("\t")
        for word in wlist:
            self.mark_word(word)
        self.of.write("\n")

    def mark_word(self, word):
        if len(word) == 1 or len(word) == 2 and word[1] == "\n":
            self.of.write("\t" + word[0] + "S")
            self.of2.write("S")
        elif len(word) == 2:
            self.of.write("\t" + word[0] + "B" + word[1] + "E")
            self.of2.write("BE")
        else:
            self.of.write("\t" + word[0] + "B")
            self.of2.write("B")
            for i in range(1, len(word) - 2):
                self.of.write(word[i] + "M")
                self.of2.write("M")
            self.of.write(word[len(word) - 1] + "E")
            self.of2.write("E")

    def close(self):
        self.f.close()
        self.of.close()
        self.of2.close()


class Statistics:
    def __init__(self, after_mark, status_file, epm_json, tpm_json, is_json):

        self.letters = 0
        self.little = 0
        self.percent = 0
        with open(after_mark, 'r') as f:
            for line in f:
                for letter in line:
                    if letter not in ["B", "M", "E", "S", "\t", "\n", " "]:
                        self.letters += 1

        self.inf = open(after_mark, "r")
        self.inf2 = open(status_file, "r")
        self.of = codecs.open(epm_json, "w", "utf-8")
        self.of2 = codecs.open(tpm_json, "w", "utf-8")
        self.of3 = codecs.open(is_json, "w", "utf-8")
        self.epm_dic = {}
        self.is_dic = {"B": 0, "M": 0, "E": 0, "S": 0}
        self.tpm_dic = {}

    def run(self):
        # EmitProbMatrix && InitStatus
        for line in self.inf:
            for letter in line:
                if letter in ["B", "S"]:
                    self.is_dic[letter] += 1
                    break
            self.do_statistics(line)

        # TransProbMatrix
        tlist = list(self.inf2)
        tstr = tlist[0]
        for i in range(0, len(tstr) - 1):
            if tstr[i] in self.tpm_dic:
                if tstr[i + 1] in self.tpm_dic[tstr[i]]:
                    self.tpm_dic[tstr[i]][tstr[i + 1]] += 1
                else:
                    self.tpm_dic[tstr[i]][tstr[i + 1]] = 1
            else:
                self.tpm_dic[tstr[i]] = {tstr[i + 1]: 1}
        self.tidy_up()
        self.of.write(json.dumps(self.epm_dic, ensure_ascii=False))
        self.of2.write(json.dumps(self.tpm_dic, ensure_ascii=False))
        self.of3.write(json.dumps(self.is_dic, ensure_ascii=False))
        self.close()

    def do_statistics(self, sentence):
        wlist = sentence.split("\t")
        for word in wlist:
            if len(word) > 0 and word[-1] == "\n":
                word = word[0:-1]
            for i in range(0, len(word), 2):
                key = word[i]
                value = word[i + 1]
                if key in self.epm_dic:
                    if value in self.epm_dic[key]:
                        self.epm_dic[key][value] += 1
                    else:
                        self.epm_dic[key][value] = 1
                else:
                    self.epm_dic[key] = {value: 1}

    def tidy_up(self):

        # for d in self.epm_dic:
        #     for key in self.epm_dic[d]:
        #         if self.epm_dic[d][key] < 8:
        #             self.little += self.epm_dic[d][key]
        # self.percent = float(self.little) / self.letters

        for d in self.epm_dic:
            for key in ["B", "M", "E", "S"]:
                if key in self.epm_dic[d]:
                    self.epm_dic[d][key] = math.log10(float(self.epm_dic[d][key]) / self.letters)
                else:
                    self.epm_dic[d][key] = math.log10(float(3) / self.letters)
        self.epm_dic["NONE"] = math.log10(float(3) / self.letters)

        for key in self.is_dic:
            if self.is_dic[key] == 0:
                self.is_dic[key] = -3.14e+100
            else:
                self.is_dic[key] = math.log10(float(self.is_dic[key]) / self.letters)

        for d in self.tpm_dic:
            for key in["B", "M", "E", "S"]:
                if key in self.tpm_dic[d]:
                    self.tpm_dic[d][key] = math.log10(float(self.tpm_dic[d][key]) / self.letters)
                else:
                    self.tpm_dic[d][key] = MIN

    def close(self):
        self.inf2.close()
        self.inf.close()
        self.of.close()
        self.of2.close()
        self.of3.close()


if __name__ == "__main__":
    start_train()



