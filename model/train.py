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
# dict big source
DICT_BIG_SOURCE = "res/dict/dict.txt.big"
# save dict big
DICT_BIG_JSON = "dict.big.json"
# dict small
DICT_SMALL_SOURCE = "res/dict/dict.txt.small"
# save dict small
DICT_SMALL_JSON = "dict.small.json"
# dict stop source
DICT_STOP_SOURCE = "res/dict/stop_words.txt"
# save stop big
DICT_STOP_JSON = "dict.stop.json"

# hmm3
# save TransProbMatrix location in there
TPM_JSON2 = "TransProbMatrix2.json"
# save EmitProbMatrix location in there
EPM_JSON2 = "EmitProbMatrix2.json"


def start_train():
    here = os.path.split(os.path.realpath(__file__))[0]
    after_mark = here + "/" + AFTER_MARK
    status_file = here + "/" + STATUS_FILE
    is_json = here + "/" + IS_JSON
    tpm_json = here + "/" + TPM_JSON
    epm_json = here + "/" + EPM_JSON
    tpm_json2 = here + "/" + TPM_JSON2
    epm_json2 = here + "/" + EPM_JSON2
    dict_source = here[0:here.rfind("/")] + "/" + DICT_BIG_SOURCE
    dict_json = here + "/" + DICT_BIG_JSON
    dict_small = here[0:here.rfind("/")] + "/" + DICT_SMALL_SOURCE
    dict_small_json = here + "/" + DICT_SMALL_JSON
    dict_stop = here[0:here.rfind("/")] + "/" + DICT_STOP_SOURCE
    dict_stop_json = here + "/" + DICT_STOP_JSON
    train_source = here[0:here.rfind("/")] + "/" + TRAIN_SOURCE
    Train(train_source, dict_source, dict_small, dict_stop, after_mark, status_file,
          is_json, tpm_json, epm_json, tpm_json2, epm_json2, dict_json,
          dict_small_json, dict_stop_json)


class Train:
    def __init__(self, train_source, dict_source, dict_small, dict_stop, after_mark, status_file, is_json,
                 tpm_json, epm_json, tpm_json2, epm_json2, dict_json, dict_small_json, dict_stop_json):
        self.train_source = train_source
        self.dict_source = dict_source
        self.after_mark = after_mark
        self.status_file = status_file
        self.is_json = is_json
        self.tpm_json = tpm_json
        self.epm_json = epm_json
        self.tpm_json2 = tpm_json2
        self.epm_json2 = epm_json2
        self.dict_json = dict_json
        self.dict_small = dict_small
        self.dict_small_json = dict_small_json
        self.dict_stop = dict_stop
        self.dict_stop_json = dict_stop_json

        self.mark = MarkSample(self.train_source, self.after_mark, self.status_file)
        self.mark.train()
        # dict
        self.dic_dealer = DictDealer(self.dict_source, self.dict_small, self.dict_stop,
                                     self.dict_json, self.dict_small_json, self.dict_stop_json )
        # hmm2
        self.statistics = Statistics(self.after_mark, self.status_file, self.epm_json, self.tpm_json, self.is_json)
        self.statistics.run()
        # hmm3
        self.statistics3 = StatisticsHMM3(self.after_mark, self.status_file, self.epm_json2, self.tpm_json2)
        self.statistics3.run()


class DictDealer:
    def __init__(self, dict_source, dict_small, dict_stop, dict_json, dict_small_json, dict_stop_json):
        self.word_dict = {}
        self.deal_files = [
            (dict_source, dict_json),
            (dict_small, dict_small_json)
        ]
        self.dict_stop = dict_stop
        self.dict_stop_json = dict_stop_json

        for files in self.deal_files:
            print(files[0])
            self.word_dict = {}
            with open(files[0], "r") as f:
                for line in f:
                    self.deal_word(line)
            with open(files[1], "w") as f:
                f.write(json.dumps(self.word_dict, ensure_ascii=False))

        with open(self.dict_stop, "r") as f:
            self.word_dict = {}
            for line in f:
                self.word_dict[line[:-1]] = 1
        with open(self.dict_stop_json, "w") as f:
            f.write(json.dumps(self.word_dict, ensure_ascii=False))
        print(self.word_dict["妳們"])

    def deal_word(self, line):
        r_list = line[0: -1].split(" ")
        dict_tmp = self.word_dict
        for ch in r_list[0]:
            if ch not in dict_tmp:
                dict_tmp[ch] = {}
            dict_tmp = dict_tmp[ch]
        dict_tmp["TIMES"] = math.log2(float(r_list[1]))



class MarkSample:
    """mark train file for every char """
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
    """hmm 2"""
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
                    self.epm_dic[d][key] = math.log2(float(self.epm_dic[d][key]) / self.letters)
                else:
                    self.epm_dic[d][key] = math.log2(float(0.1) / self.letters)
        self.epm_dic["NONE"] = math.log2(float(0.1) / self.letters)

        for key in self.is_dic:
            if self.is_dic[key] == 0:
                self.is_dic[key] = -3.14e+100
            else:
                self.is_dic[key] = math.log2(float(self.is_dic[key]) / self.letters)
        self.is_dic["NONE"] = math.log2(float(0.1) / self.letters)

        for d in self.tpm_dic:
            for key in["B", "M", "E", "S"]:
                if key in self.tpm_dic[d]:
                    self.tpm_dic[d][key] = math.log2(float(self.tpm_dic[d][key]) / self.letters)
                else:
                    self.tpm_dic[d][key] = MIN

    def close(self):
        self.inf2.close()
        self.inf.close()
        self.of.close()
        self.of2.close()
        self.of3.close()


class StatisticsHMM3(Statistics):
    """hmm 3"""
    def __init__(self, after_mark, status_file, epm_json2, tpm_json2):
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
        self.of4 = codecs.open(epm_json2, "w", "utf-8")
        self.of5 = codecs.open(tpm_json2, "w", "utf-8")
        self.tpm_dic2 = {}
        self.epm_dic2 = {}

    def run(self):
        # EmitProbMatrix && InitStatus
        for line in self.inf:
            self.do_statistics(line)
        # TransProbMatrix

        tlist = list(self.inf2)
        tstr = tlist[0]
        for i in range(0, len(tstr) - 2):

            # read second status
            # t[i] {"A":?}
            # t[i][j] {"A":{"A":?}}
            # t[i][j][k] {"A" :{"A" : {"A"}}}
            if tstr[i] in self.tpm_dic2:
                if tstr[i + 1] not in self.tpm_dic2[tstr[i]]:
                    self.tpm_dic2[tstr[i]][tstr[i + 1]] = {}
            else:
                self.tpm_dic2[tstr[i]] = {}
                self.tpm_dic2[tstr[i]][tstr[i + 1]] = {}

            # read second status
            if tstr[i + 2] in self.tpm_dic2[tstr[i]][tstr[i + 1]]:
                self.tpm_dic2[tstr[i]][tstr[i + 1]][tstr[i + 2]] += 1
            else:
                self.tpm_dic2[tstr[i]][tstr[i + 1]][tstr[i + 2]] = 1
        self.tidy_up()
        self.of4.write(json.dumps(self.epm_dic2, ensure_ascii=False))
        self.of5.write(json.dumps(self.tpm_dic2, ensure_ascii=False))

        self.close()

    def do_statistics(self, sentence):
        wlist = sentence.split("\t")
        sentence = "".join(wlist)
        if len(sentence) > 0 and sentence[-1] == "\n":
            sentence = sentence[0:-1]
        for i in range(2, len(sentence), 2):
            key = sentence[i - 1]
            key1 = sentence[i + 1]
            value = sentence[i]

            if key in self.epm_dic2:
                if key1 in self.epm_dic2[key]:
                    if value in self.epm_dic2[key][key1]:
                        self.epm_dic2[key][key1][value] += 1
                    else:
                        self.epm_dic2[key][key1][value] = 1
                else:
                    self.epm_dic2[key][key1] = {value: 1}
            else:
                self.epm_dic2[key] = {key1: {value: 1}}

    def tidy_up(self):
        for key1 in self.epm_dic2:
            for key2 in self.epm_dic2[key1]:
                for key3 in self.epm_dic2[key1][key2]:
                    self.epm_dic2[key1][key2][key3] = math.log2(float(self.epm_dic2[key1][key2][key3]) / self.letters)
        self.epm_dic2["NONE"] = math.log2(float(0.1) / self.letters)

        for key1 in self.tpm_dic2:
            for key2 in self.tpm_dic2[key1]:
                for key3 in self.tpm_dic2[key1][key2]:
                        self.tpm_dic2[key1][key2][key3] = math.log2(float(self.tpm_dic2[key1][key2][key3]) / self.letters)

    def close(self):
        self.inf.close()
        self.inf2.close()
        self.of4.close()
        self.of5.close()


if __name__ == "__main__":
    start_train()




