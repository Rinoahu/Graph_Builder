#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-02-08 12:14:30
from math import log
from rpython.rlib import rrandom

class Seq:
    def __init__(self, seq, k = 5):
        self.seq = seq
        self.k = k
        self.N = len(seq)

    def __getitem__(self, i):
        return self.seq[i: i + self.k]

    def __len__(self):
        return self.N

# define some constant number
MIN = 7
MED = 23
MAX = 41

random = rrandom.Random(10).random

# swap 2 selected elem in a list
def swap(x, i, j):
    x[i], x[j] = x[j], x[i]

# in-place sort
def insort(x, y, l, r):
    for i in xrange(l, r):
        v = x[i]
        pivot = y[v]
        j = i - 1
        while j >= l:
            if y[x[j]] <= pivot:
                break
            x[j + 1] = x[j]
            j -= 1

        x[j + 1] = v

# partition function of quicksort
def partition(x, y, l, r, m):
    t = x[l]
    pivot = y[t]
    i, j = l, r + 1
    while 1:
        i += 1
        while i <= r and y[x[i]] < pivot:
            i += 1
        j -= 1
        while y[x[j]] > pivot:
            j -= 1
        if i > j:
            break
        swap(x, i, j)

    swap(x, l, j)
    return j

def quicksort(x, y, l, r):
    if r <= l:
        return
    else:
        gap = r - l + 1
        if gap < MIN:
            insort(x, y, l, r + 1)
            return

        elif MIN == gap:
            m = l + gap // 2

        else:
            m = l + int(random() * gap)

        swap(x, l, m)
        med = partition(x, y, l, r, m)
        quicksort(x, y, l, med - 1)
        quicksort(x, y, med + 1, r)

# the main function of qsort
def qsort(y):
    x = range(len(y))
    quicksort(x, y, 0, len(y) - 1)
    return x

def fac(N):
    if N <= 1:
        return 0
    else:
        return log(N) + fac(N - 1)


def entry_point(argv):
    N = int(argv[1])
    #print fac(N)
    #a = [random() for elem in xrange(N)]
    s = 'asdfasdfasdasdf' * N
    a = Seq(s, 10)
    #return 0
    b = qsort(a)
    for i in xrange(N - 1):
        if a[b[i]] > a[b[i + 1]]:
            print 'error'
            break
    print 'correct'
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    import sys
    entry_point(sys.argv)
