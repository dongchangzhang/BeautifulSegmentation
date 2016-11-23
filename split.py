import os
import re
import json
import shutil
from constant import *


status = 0


def split_file(file):
    spliter = Spliter()
    spliter.split_for_file(file)


def split_sentence(sentence):
    spliter = Spliter()
    return spliter.split_for_sentence(sentence)


def get_status():
    return status


class Spliter:

    def __init__(self):
        self.is_dic = {}
        self.tpm_dic = {}
        self.epm_dic = {}
        self.mark = {0: "B", 1: "M", 2: "E", 3: "S"}
        with open(IS_JSON, "r") as f:
            self.is_dic = json.load(f)
        with open(TPM_JSON, "r") as f:
            self.tpm_dic = json.load(f)
        with open(EPM_JSON, "r") as f:
            self.epm_dic = json.load(f)

    def split_for_file(self, file):
        global status
        try:
            with open(file, "r") as f:
                out_file = OUT_DIR + file[file.rfind("/"):] + ".out.txt"
                with open(out_file, "w") as out:
                    for sentence in f:
                        status += 1
                        out.write(self.split_for_sentence(sentence) + "\n")
                shutil.copy(out_file, TMP_FILE)
        except:
            print("Not find file: " + file)

    def split_for_sentence(self, sentence):
        # to prepare
        sentence_len = len(sentence)
        weight = [([MIN] * sentence_len) for i in range(0, 4)]
        path = [([-1] * sentence_len) for i in range(0, 4)]

        # init weight
        if sentence[0] not in self.epm_dic:
            value = {
                "B": self.epm_dic["NONE"],
                "M": MIN,
                "E": MIN,
                "S": self.epm_dic["NONE"]
            }
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
                        tmp = weight[k][i - 1] + self.tpm_dic[self.mark[k]][self.mark[j]] + self.epm_dic["NONE"]
                    else:
                        tmp = weight[k][i-1] + self.tpm_dic[self.mark[k]][self.mark[j]] + self.epm_dic[sentence[i]][self.mark[j]]
                    if tmp > weight[j][i]:
                        weight[j][i] = tmp
                        path[j][i] = k

        # confirm back point

        if weight[2][sentence_len - 1] > weight[3][sentence_len - 1]:
            back_point = 2
        else:
            back_point = 3

        rmark_result = ""

        for i in range(0, sentence_len - 1):

            rmark_result += self.mark[back_point]
            back_point = path[back_point][sentence_len - 1 - i]
        rmark_result += self.mark[back_point]
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

class Spliter2(Spliter):
    def __init__(self):
        super(Spliter2, self).__init__()
        with open(TPM_JSON2, "r") as f:
            self.tpm_dic2 = json.load(f)
        with open(EPM_JSON2, "r") as f:
            self.epm_dic2 = json.load(f)

    def split_for_sentence(self, sentence):
        # to prepare
        sentence_len = len(sentence)
        weight = [[([MIN] * sentence_len) for i in range(0, 4)] for j in range(0, 4)]
        path = [[([-1] * sentence_len) for i in range(0, 4)] for j in range(0, 4)]
        # init weight
        for i in range(0, 4):
            for j in range(0, 4):
                try:
                    a = self.epm_dic[j][sentence[0]]
                except:
                    a = self.is_dic["NONE"]
                try:
                    b = self.epm_dic[j][i][sentence[1]]
                except:
                    b = self.is_dic["NONE"]
                try:
                    c = self.tpm_dic[j][i]
                except:
                    c = self.is_dic["NONE"]

                weight[j][i][1] = self.is_dic[self.mark[j]] + a + b + c
        # every word
        # weight[i][j][x] last status; now status; the word
        for i in range(2, sentence_len):
            # every may status
            for j in range(0, 4):
                # every last char status
                for k in range(0, 4):
                    # every last last status
                    for l in range(0, 4):
                        try:
                            a = self.tpm_dic2[self.mark[l]][self.mark[k]][self.mark[j]]
                        except:
                            a = self.is_dic["NONE"]
                        try:
                            b = self.epm_dic2[self.mark[l]][self.mark[k]][sentence[i]]
                        except:
                            b = self.is_dic["NONE"]

                        tmp = weight[l][k][i - 1] + a + b

                    if tmp > weight[k][j][i]:
                        weight[k][j][i] = tmp
                        path[k][j][i] = l

        # find max end
        tmp = MIN
        # now
        end_i = 0
        # last
        end_j = 0
        for i in range(0, 4):
            for j in range(0, 4):

                if weight[j][i][sentence_len - 1] > tmp:
                    tmp = weight[j][i][sentence_len - 1]
                    end_i = i
                    end_j = j


        # back
        rmark_result = ""
        rmark_result += self.mark[end_i]
        rmark_result += self.mark[end_j]
        for i in range(0, sentence_len - 2):
            # + now
            tmp = path[end_j][end_i][sentence_len - i - 1]
            rmark_result += self.mark[tmp]
            # get last
            end_i = end_j
            end_j = tmp
        print(rmark_result[::-1])


class DictSpliter:
    def __init__(self):
        self.re_han = re.compile(u"([\u4E00-\u9FA5a-zA-Z0-9+#&\._]+)", re.U)
        self.graph = {}
        with open(DICT_BIG_JSON, "r") as f:
            self.word_dict_big = json.load(f)
        with open(DICT_SMALL_JSON, "r") as f:
            self.word_dict_small = json.load(f)

    def deal_sentence(self, sentence):
        original_sentence = self.re_han.findall(sentence)
        result = ""
        for sen in original_sentence:
            result += self.deal_final_sentence(sen) + "/"
        return result

    def deal_final_sentence(self, sentence):
        result = ""
        sen_len = len(sentence)
        for i in range(0, sen_len):
            location = sen_len - i - 1
            if location not in self.graph:
                self.graph[location] = {}
            times = 0
            tmp = location
            pos = location
            dict_tmp = self.word_dict_small
            while tmp < sen_len:
                if sentence[tmp] in dict_tmp:
                    if "TIMES" in dict_tmp[sentence[tmp]]:
                        times = dict_tmp[sentence[tmp]]["TIMES"]
                        pos = tmp
                    dict_tmp = dict_tmp[sentence[tmp]]
                    tmp += 1

                else:
                    break

            self.graph[location][pos] = times
        # deal graph
        print(self.graph)
        mark = [-1] * sen_len
        dijkstra = [[i, -1, 0] for i in range(0, sen_len)]
        for i in range(0, sen_len):
            for j in self.graph[i]:
                dijkstra[j][2] = self.graph[i][j]
                dijkstra[j][1] = i
        print(dijkstra)
        return result


if __name__ == "__main__":
    test = Spliter()
    print(test.split_for_sentence("小明毕业于清华大学"))
    # # test.split_for_file("/home/me/GitHub/ChineseWS/res/test/judge.data.1")
    # tests = DictSpliter()
    # tests.deal_sentence("刘挺拔出宝剑")
