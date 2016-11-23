#!/usr/bin/env python3
import os
import json
import math
import codecs
from constant import *


def start_train():
    Train()


class Train:
    def __init__(self):

        self.mark = MarkSample()
        self.mark.train()
        # dict
        self.dic_dealer = DictDealer()
        # hmm2
        self.statistics = Statistics()
        self.statistics.run()
        # hmm3
        self.statistics2 = StatisticsHMM2()
        self.statistics2.run()


class DictDealer:
    def __init__(self):
        self.word_dict = {}
        self.deal_files = [
            (DICT_BIG_SOURCE, DICT_BIG_JSON),
            (DICT_SMALL_SOURCE, DICT_SMALL_JSON)
        ]
        self.dict_stop = DICT_STOP_SOURCE
        self.dict_stop_json = DICT_STOP_JSON

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
    def __init__(self):
        self.f = open(TRAIN_SOURCE, "r")
        self.of = open(AFTER_MARK, "w")
        self.of2 = open(STATUS_FILE, "w")

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
    def __init__(self):

        self.letters = 0
        self.little = 0
        self.percent = 0
        with open(AFTER_MARK, 'r') as f:
            for line in f:
                for letter in line:
                    if letter not in ["B", "M", "E", "S", "\t", "\n", " "]:
                        self.letters += 1

        self.inf = open(AFTER_MARK, "r")
        self.inf2 = open(STATUS_FILE, "r")
        self.of = codecs.open(EPM_JSON, "w", "utf-8")
        self.of2 = codecs.open(TPM_JSON, "w", "utf-8")
        self.of3 = codecs.open(IS_JSON, "w", "utf-8")
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


class StatisticsHMM2(Statistics):
    """hmm 3"""
    def __init__(self):
        self.letters = 0
        self.little = 0
        self.percent = 0
        with open(AFTER_MARK, 'r') as f:
            for line in f:
                for letter in line:
                    if letter not in ["B", "M", "E", "S", "\t", "\n", " "]:
                        self.letters += 1
        self.inf = open(AFTER_MARK, "r")
        self.inf2 = open(STATUS_FILE, "r")
        self.of4 = codecs.open(EPM_JSON2, "w", "utf-8")
        self.of5 = codecs.open(TPM_JSON2, "w", "utf-8")
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




