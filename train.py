#!/usr/bin/env python3
import re
import os
import json
import math
import codecs
from constant import *

TRAIN_FILES = os.listdir(TRAIN_SOURCES)
TRAIN_FILES_LIST = [os.path.join(TRAIN_SOURCES, x) for x in TRAIN_FILES]

def start_train():
    Train()

class Train:
    def __init__(self):
        # dict
        self.dic_dealer = DictDealer()
         # hmm2
        self.mark = MarkSample()
        self.mark.train()
        self.statistics = Statistics()
        self.statistics.run()
  
class DictDealer:
    def __init__(self):
        self.r = re.compile(r'([^\s]*)[\s\t]+([\d]*)')
        self.word_dict = {}
        self.deal_files = [
            DICT_BIG_SOURCE,
            DICT_SMALL_SOURCE,
            DICT_OTHER_SOURCE,
            DICT_IDF_SOURCE,
        ]
        self.outf = DICT_BIG_JSON

        self.deal_files_small = [
            DICT_OTHER_SOURCE,
            DICT_SMALL_SOURCE,
        ]

        self.outf_small = DICT_SMALL_JSON

        self.deal_files_test = [
            DICT_OTHER_SOURCE,
        ]
        self.outf_test = DICT_TEST_JSON

        # deal big
        self.deal_dict(self.deal_files, self.outf)
        # deal small
        self.deal_dict(self.deal_files_small, self.outf_small)
         # deal test
        self.deal_dict(self.deal_files_test, self.outf_test)

    def deal_dict(self, files, out):
        self.word_dict = {}

        print('start deal dict...')
        for file in files:
            print('dealing', file)
            with open(file, 'r') as f:
                for line in f:
                    rg = self.r.match(line)
                    self.word_dict[rg.group(1)] = rg.group(2)
        print('saving dict to', out)
        with open(out, 'w') as f:
            f.write(json.dumps(self.word_dict, ensure_ascii=False))


class MarkSample:
    """mark train file for every char """
    def __init__(self):

        self.of = open(AFTER_MARK, "w")
        self.of2 = open(STATUS_FILE, "w")

    def train(self):
        print('training hmm model...')
        for file in TRAIN_FILES_LIST:
            print('dealing', file)
            with open(file, 'r') as f:
                for line in f:
                    if line[-1] == '\n' or line[-1] == '\t':
                        line = line[:-1]
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
        elif len(word) == 1 and word == '\n':
            pass
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


if __name__ == "__main__":
    start_train()




