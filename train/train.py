#!/usr/bin/env python3


import sys
import json
import math
import codecs

sys.path.append("..")

from config import config


class MarkSample:

    def __init__(self,
                 train_file,
                 out_file="../out/letter_mark.txt",
                 out_file2="../out/status.txt"):
        self.f = open(train_file, "r")
        self.of = open(out_file, "w")
        self.of2 = open(out_file2, "w")

    def train(self):

        for line in self.f:
            self.deal_sentence(line)

        self.close()

    def deal_sentence(self,  sentence):

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

    def __init__(self,
                 in_file="../out/letter_mark.txt",
                 in_file2="../out/status.txt",
                 out_file="../out/EmitProbMatrix.json",
                 out_file2="../out/TransProbMatrix.json",
                 out_file3="../out/InitStatus.json"):

        self.letters = 0
        with open(in_file, 'r') as f:
            for line in f:
                for letter in line:
                    if letter not in ["B", "M", "E", "S", "\t", "\n", " "]:
                        self.letters += 1

        self.inf = open(in_file, "r")
        self.inf2 = open(in_file2, "r")
        self.of = codecs.open(out_file, "w", "utf-8")
        self.of2 = codecs.open(out_file2, "w", "utf-8")
        self.of3 = codecs.open(out_file3, "w", "utf-8")
        self.epm_dic = {}
        self.is_dic = {"B": 0, "M": 0, "E": 0, "S": 0}
        self.tpm_dic = {}

    def run(self):
        # EmitProbMatrix && InitStatus
        for line in self.inf:
            for letter in line:
                if letter in ["B", "S"]:
                    self.is_dic[letter] += 1
                    break;
            self.do_statistics(line)

        # TransProbMatrix
        tlist = list(self.inf2)
        tstr = tlist[0]
        print(tstr)
        for i in range(0, len(tstr) - 1):
            print(tstr[i] + tstr[i + 1])
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
        for d in self.epm_dic:
            for key in self.epm_dic[d]:
                self.epm_dic[d][key] = math.log2(float(self.epm_dic[d][key]) / self.letters)
        for key in self.is_dic:
            self.is_dic[key] = math.log2(float(self.is_dic[key]) / self.letters)
        for d in self.tpm_dic:
            for key in self.tpm_dic[d]:
                self.tpm_dic[d][key] = math.log2(float(self.tpm_dic[d][key]) / self.letters)

    def close(self):
        self.inf2.close()
        self.inf.close()
        self.of.close()
        self.of2.close()
        self.of3.close()

if __name__ == "__main__":
    test = MarkSample(config.TRAIN_LOCATION)
    test.train()

    test2 = Statistics()
    test2.run()



