from constant import *

def check_result(data, result):
    print("Start checking", result, 'by compare with', data)
    result = CheckResult(data, result)
    return result.get_result()


class CheckResult():
    def __init__(self, data, result):
        self.data = data
        self.result = result

    def get_result(self):
        # R P F
        data_list = []
        result_list = []
        rec = 0

        with open(self.data, 'r') as f:

            for line in f:
                if line[-1] == '\n':
                    line = line[:-1]
                tmp = line.split('\t')
                while '' in tmp:
                    tmp.remove('')
                data_list.extend(tmp)

        data_times = len(data_list)
        data_string = "\t".join(data_list)
        len1 = len(data_string)

        with open(self.result, 'r') as f:
            for line in f:
                if line[-1] == '\n':
                    line = line[:-1]
                tmp = line.split('\t')
                while '' in tmp:
                    tmp.remove('')
                if len(tmp) > 0:
                    result_list.extend(tmp)
        result_times = len(result_list)
        result_string = "\t".join(result_list)
        len2 = len(result_string)

        last = True
        i = 0
        j = 0

        while True:
            if len1 == i or len2 == j:
                break
            if last is True and data_string[i] == '\t' and result_string[j] == '\t':
                rec += 1
                i += 1
                j += 1
            elif last is False and data_string[i] == '\t' and result_string[j] == '\t':
                last = True
                i += 1
                j += 1
            elif data_string[i] == '\t' and result_string[j] != '\t':
                last = False
                i += 1
            elif data_string[i] != '\t' and result_string[j] == '\t':
                last = False
                j += 1
            else:
                i += 1
                j += 1

        P = rec / result_times
        R = rec / data_times
        F = P * R * 2 / (P + R)

        result = P, R, F
        print(result)

        return result


if __name__ == "__main__":
    # 处理第一个训练数据的正确率 TEST1, JUDGE2
    # 处理第二个 TEST2， JUDGE2
    check_result(TEST1, JUDGE1)
    check_result(TEST2, JUDGE2)
