# -*- coding:utf-8 -*-
# !/usr/bin/env python3

import sys
import time


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self):
        self.count += 1

    def log(self, s):
        sys.stdout.write(' ' * (self.width*2) + '\r')
        sys.stdout.flush()
        print(s)
        progress = self.width * self.count // self.total
        sys.stdout.write('{0:6}/{1:6}: '.format(self.count, self.total))
        sys.stdout.write('▇' * progress + '-' * (self.width - progress)
                         + ' {0:6.2f}%/100%'.format(float(self.count * 100) / self.total) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


def test():
    bar = ProgressBar(total=10000)
    for i in range(10000):
        bar.move()
        bar.log('We have arrived at: ' + str(i + 1))
        time.sleep(0.0001)
if __name__ == "__main__":
    test()