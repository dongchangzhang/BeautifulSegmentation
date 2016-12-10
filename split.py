import os
import re
import json
import time
import shutil
from constant import *

status = 0

def get_status():
    return status

def split_sentence(sentence, mode=False, test_mode=False):
    sp = Spliter(mode, test_mode)
    return sp.start(sentence)

def split_file(file, mode=False, test_mode=False):
    sp = Spliter(mode, test_mode)
    sp.split_for_file(file)

class Spliter:
    def __init__(self, mode=False, test_mode=False):

        self.word_dict = {}
        self.max_len = MAX_LEN_L
        self.max = MAX_LEN_L
        self.count = 0
        self.h = HMM()
        self.load_dict(mode, test_mode)
        self.netadd = re.compile(r'(http://[0-9a-zA-Z./]+|https://[0-9a-zA-Z./]+|ftp://[0-9a-zA-Z./]+)')
        self.re_han = re.compile(r"([\u4E00-\u9FA5]+)", re.U)

    def count_char(self, file):
        with open(file, 'r') as f:
            l = list(f)
            text = ''.join(l)
            self.count = len(text)
        print('in file', file, ',the number of char is', len(text))

    # mode is True -> word will be longer, else, smaller
    # test_mode is True -> just use the dict for two test file
    def load_dict(self, mode=True, test_mode=False):
        if mode is True and not test_mode:
            print('working with big mode')
            with open(DICT_BIG_JSON, "r") as f:
                self.word_dict = json.load(f)
            self.max_len = MAX_LEN_L
            self.max = MAX_LEN_L
        elif mode is False and not test_mode:
            print('working with small mode')
            with open(DICT_SMALL_JSON, "r") as f:
                self.word_dict = json.load(f)
            self.max_len = MAX_LEN_S
            self.max = MAX_LEN_S
        else:
            print('working with test mode')
            with open(DICT_TEST_JSON, "r") as f:
                self.word_dict = json.load(f)
            self.max_len = MAX_LEN_S
            self.max = MAX_LEN_S

    # split for file
    def split_for_file(self, file):
        global status
        status = 0
        starttime = time.clock()
        self.count_char(file)
        with open(file, "r") as f:
            out_file = OUT_DIR + file[file.rfind("/"):] + ".out.txt"
            with open(out_file, "w") as out:
                for sentence in f:
                    status += 1
                    out.write(self.start(sentence) + "\n")
            shutil.copy(out_file, TMP_FILE)
        endtime = time.clock()
        print('use time', (endtime - starttime), 'clocks')


    # split for sentence
    def start(self, line):
        nrec1, pmr, nlist1 = self.positive_match(line)
        nrec2, rmr, nlist2 = self.reverse_match(line)
        result , nl = self.bidirectional_match(nrec1, pmr, nlist1, nrec2, rmr, nlist2)

        return self.after_deal(result, nl)

    def after_deal(self, result, nl):
        # remove \n in list
        while '\n' in result:
            
            try:
                nl.remove(result.index('\n'))
            except:
                print('can not remove')
            result.remove('\n')
       # deal word which not in dict by hmm 
        for i in nl:
            try:
                tmp = self.re_han.findall(result[i])
                if len(tmp) != 0:
                    
                    tmp_list = self.re_han.split(result[i])
                    tmp_str = ''
                    for s in tmp_list:
                        if s != '':
                            if len(self.re_han.findall(result[i])) != 0:
                                print(1, tmp_str)
                                tmp_str += self.h.split_for_sentence(s) + '\t'
                            else:
                                tmp_str += s + '\t'
                                print(2, tmp_str)
                    result[i] = tmp_str[:-1]
                    print(result[i])
            except:
                print('Error')
        # deal one chars
        # start = -1
        # end = -1
        # str_tmp = ''
        # r_tmp = []
        # for i in range(0, len(result)):
        #     print(result[i])
        #     if len(result[i]) == 1 and start == -1:
        #         str_tmp += result[i]
        #         start = i
        #         end = start + 1
        #     elif len(result[i]) == 1:
        #         str_tmp += result[i]
        #         end += 1
        #     else:
        #         if start != -1:
        #             print(str_tmp)
        #             r_tmp.append(self.h.split_for_sentence(str_tmp))
        #             str_tmp = ''
        #             start = -1
        #             end = -1
        #         r_tmp.append(result[i])
        # if str_tmp != '':
        #     r_tmp.append(self.h.split_for_sentence(str_tmp))
        #     str_tmp = ''
        #     start = -1
        #     end = -1

        # print(r_tmp)


        # deal net add
        result = '\t'.join(result)
        print(result)
        tmp = self.netadd.findall(result)
        for add in tmp:
            result = result.replace(add, '\t' + add + '\t')
            # print(result)
        while result[-1] == '\t':
            result = result[:-1]
        
        print('result', result)
        return result

    # 正向匹配
    def positive_match(self, line):
        result = []
        not_rec = 0
        not_rec_list = []
        llen = len(line)
        self.max_len = self.max

        if llen < self.max_len:
            self.max_len = llen

        start = 0
        end = self.max_len
        if end > llen:
            end = llen
        tmp = ''

        while start < llen:
            if line[start:end] in self.word_dict:
                if tmp != '':
                    not_rec_list.append(len(result))
                    result.append(tmp)
                    tmp = ''
                result.append(line[start:end])
                start = end
                if end + self.max_len > llen:
                    end = llen
                else:
                    end += self.max_len
            else:
                if start == end:
                    not_rec += 1
                    tmp += line[start:end + 1]
                    # result.append(line[start:end + 1])
                    start += 1
                    end = start + self.max_len
                    if end > llen:
                        end = llen
                end -= 1
        if tmp != '':
            not_rec_list.append(len(result))
            result.append(tmp)
            tmp = ''
        print('positive', result)
        return not_rec, result, not_rec_list
    #逆向匹配
    def reverse_match(self, line):
        result = []
        not_rec = 0
        not_rec_list = []
        llen = len(line)
        self.max_len = self.max

        if llen < self.max_len:
            self.max_len = llen
        start = llen - self.max_len
        if start < 0:
            start = 0
        end = llen
        tmp = ''

        while end > 0:

            if line[start:end] in self.word_dict:
                if tmp != '':
                    not_rec_list.insert(0, len(result))
                    result.insert(0, tmp)
                    tmp = ''
                result.insert(0, line[start:end])
                end = start
                if start - self.max_len < 0:
                    start = 0
                else:
                    start -= self.max_len
            else:
                if start == end:
                    not_rec += 1
                    tmp = line[start-1:end] + tmp
                    # result.insert(0, line[start-1:end])
                    end -= 1
                    start = end - self.max_len
                    if start < 0:
                        start = 0
                start += 1
        if tmp != '':
            not_rec_list.insert(0, len(result))
            result.insert(0, tmp)
            tmp = ''
        for i in range(0, len(not_rec_list)):
            not_rec_list[i] = len(result) - not_rec_list[i] - 1
        print('reverse', result)
        return not_rec, result, not_rec_list
    # 双向匹配
    def bidirectional_match(self, n1, l1, nl1, n2, l2, nl2):
        len1 = len(l1)
        len2 = len(l2)

        if len1 < len2:
            return l1, nl1
        elif len1 > len2:
            return l2, nl2
        else:
            if l1 == l2:
                return l2, nl2
            elif n1 < n2:
                return l1, nl1
            else:
                return l2, nl2


class HMM:

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
       
        try:
            with open(file, "r") as f:
                out_file = OUT_DIR + file[file.rfind("/"):] + ".out.txt"
                with open(out_file, "w") as out:
                    for sentence in f:
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

if __name__ == "__main__":
    # 使用学长的字典进行测试，将test_mode置为True
    a = Spliter(test_mode=True)
    print('使用学长词典')
    a.split_for_file(FOR_TEST1)

    a.split_for_file(FOR_TEST1)

    print(a.start("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"))
    print(a.start('中华人民共和国国家主席习近平一言既出驷马难追喜欢中国互联网络信息中心'))
    # 使用更多词语的小颗粒度的分词方式
    print('小颗粒模式')
    a = Spliter()
    print(a.start("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"))
    print(a.start('中华人民共和国国家主席习近平一言既出驷马难追喜欢中国互联网络信息中心'))

    # 使用大颗粒度的分词方式
    print('大颗粒模式')
    a = Spliter(mode=True)
    print(a.start("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"))
    print(a.start('中华人民共和国国家主席习近平一言既出驷马难追喜欢中国互联网络信息中心'))

    h = HMM()
    print(h.split_for_sentence('为人民办公益'))



