#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-13 15:34:46

# from array import array
import sys
import os

from math import sqrt, erf, exp, pow, log
import math
import itertools
# from itertools import izip
#from struct import pack
from random import random, seed
from rpython.rtyper.lltypesystem.module.ll_math import ll_math_log as log
from rpython.rtyper.lltypesystem.module.ll_math import ll_math_log10 as log10
from rpython.rtyper.lltypesystem.module.ll_math import ll_math_pow as pow
from rpython.rlib import rrandom
from rpython.rlib.rfloat import erfc
from rpython.rtyper.lltypesystem.rffi import r_ushort, r_int
from rpython.rlib.rarithmetic import intmask, r_uint32, r_uint, string_to_int
from rpython.rlib.rfloat import string_to_float
from rpython.rlib import rfloat
from rpython.rlib import rfile
from rpython.rlib import rmmap
from rpython.rlib.listsort import TimSort
from rpython.rlib import listsort
from rpython.rlib import rstring
from rpython.rlib.rstruct.runpack import runpack as unpack
from time import time, sleep
from rpython.rlib import rgc


from time import time, sleep
import gc
from heapq import heappush, heappop, heapreplace, heapify
#from struct import pack


# define some constant number
MIN = 7
#MIN = 13
MED = 23
MAX = 41

random = rrandom.Random(10).random

# swap 2 selected elem in a list


def swap(x, i, j):
    x[i], x[j] = x[j], x[i]

# in-place sort


def insort(x, l, r, key=lambda x: x):
    for i in xrange(l, r):
        v = x[i]
        pivot = key(v)
        j = i - 1
        while j >= l:
            if key(x[j]) <= pivot:
                break
            x[j + 1] = x[j]
            j -= 1

        x[j + 1] = v

# partition function of quicksort


def partition(x, l, r, m, key=lambda x: x):
    t = x[l]
    pivot = key(t)
    i, j = l, r + 1
    while 1:
        i += 1
        while i <= r and key(x[i]) < pivot:
            i += 1
        j -= 1
        while key(x[j]) > pivot:
            j -= 1
        if i > j:
            break
        swap(x, i, j)

    swap(x, l, j)
    return j

# recursion version of quicksort


def quicksort(x, l, r, key=lambda x: x):
    if r <= l:
        return
    else:
        gap = r - l + 1
        if gap < MIN:
            insort(x, l, r + 1, key)
            return

        elif MIN == gap:
            m = l + gap // 2

        else:
            m = l + int(random() * gap)

        swap(x, l, m)
        med = partition(x, l, r, m, key)
        quicksort(x, l, med - 1, key)
        quicksort(x, med + 1, r, key)

# the main function of qsort


def qsort(x, key=lambda x: x):
    quicksort(x, 0, len(x) - 1, key)


# the double linked-list for int
class vertex0:

    def __init__(self, val, rad=0):
        self.val = val
        self.rad = rad
        self.prev = None
        self.next = None



class llist:

    def __init__(self, iterable):
        self.first = self.last = p = None
        self.N = 0
        for i in iterable:
            node = vertex(i)
            if self.N == 0:
                self.first = self.last = node
            else:
                self.last.next = node
                self.last = self.last.next

            self.N += 1

    def __len__(self):
        return self.N

    # pop last
    def pop(self):
        #assert self.last != None
        if self.N > 0:
            node = self.last
            self.last = self.last.prev
            self.N -= 1
            return node

    # append
    def append(self, val):
        node = vertex(val)
        if self.N > 0:
            self.last.next = node
            self.last = node
        else:
            self.first = self.last = node

        self.N += 1
    # extend

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    # pop left
    def popleft(self):
        #assert self.first != None
        if self.N > 0:
            node = self.first
            self.first = self.first.next
            self.N -= 1
            return node

    # pop left
    def appendleft(self, val):
        node = vertex(val)
        if self.N > 0:
            node.next = self.first
            self.first = node
        else:
            self.first = self.last = node
        self.N += 1


# the double linked-list for int
class vtx_nd:

    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class llist_nd:

    def __init__(self, iterable):
        self.first = self.last = p = None
        self.N = 0
        for i in iterable:
            node = vtx_nd(i)
            if self.N == 0:
                self.first = self.last = node
            else:
                self.last.next = node
                self.last = self.last.next

            self.N += 1

    def __len__(self):
        return self.N

    # pop last
    def pop(self):
        #assert self.last != None
        if self.N > 0:
            node = self.last
            self.last = self.last.prev
            self.N -= 1
            return node

    # append
    def append(self, val):
        node = vtx_nd(val)
        if self.N > 0:
            self.last.next = node
            self.last = node
        else:
            self.first = self.last = node

        self.N += 1
    # extend

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    # pop left
    def popleft(self):
        #assert self.first != None
        if self.N > 0:
            node = self.first
            self.first = self.first.next
            self.N -= 1
            return node

    # pop left
    def appendleft(self, val):
        node = vtx_nd(val)
        if self.N > 0:
            node.next = self.first
            self.first = node
        else:
            self.first = self.last = node
        self.N += 1


# map function
def map(fuc, arr):
    #n = len(arr)
    # return [fuc(arr[elem]) for elem in xrange(n)]
    return [fuc(elem) for elem in arr]


# the izip function
def izip(seqs):
    iseqs = [iter(elem) for elem in seqs]
    while 1:
        try:
            yield [seq.next() for seq in iseqs]
        except:
            break

# the pack


def rpack(dtype, val):
    t = dtype.lower()
    if t == 'h':
        n = 2
    elif t == 'i':
        n = 4
    elif t == 'l':
        n = 8
    else:
        n = 1

    string = [''] * n
    for i in xrange(n):
        string[i] = chr(val & 0xFF)
        val = val >> 8

    return ''.join(string)

# find the min of a list


def Min(L):
    n = len(L)
    if n <= 1:
        return 0
    else:
        flag = L[0]
        for i in xrange(1, n):
            flag = L[i] < flag and L[i] or flag

    return flag

# find the min of a list


def Max(L):
    n = len(L)
    if n <= 1:
        return 0
    else:
        flag = L[0]
        for i in xrange(1, n):
            flag = L[i] > flag and L[i] or flag

    return flag

# open a file
# readline from an open file
# def fopen(name, chk = 128):


def readline(f, chk=128):

    #qry = args[0]
    #f = open(name, 'r')
    c = ''
    #b = []
    while 1:
        a = f.read(1024 * 1024 * chk)
        if not a:
            break
        # print a

        b = a.split('\n')
        # yield b
        b[0] = c + b[0]
        for line in b[:-1]:
            yield '%s\n' % line

        c = b[-1]

    # f.close()

# use rmmap to make realine code simple


def readline_mmap(f):
    handle = rmmap.mmap(f.fileno(), 0, access=rmmap.ACCESS_READ)
    for i in xrange(handle.size):
        line = handle.readline()
        if line != '':
            yield line
        else:
            break


class Seq:

    def __init__(self, id='', seq='', description='', qual=''):
        self.id = id
        self.seq = seq
        self.description = description
        self.qual = qual

    def update(self, id='', seq='', description='', qual=''):
        self.id = id
        self.seq = seq
        self.description = description
        self.qual = qual


# parse the fastq or fasta
# def parse(f, mode = 'fastq'):
def parse(f, dtype='fastq'):

    seq = Seq()
    output = []
    # for i in f:
    for i in readline_mmap(f):
        # print 'seq is', i
        if len(output) == 4:
            #seq.id, seq.seq, seq.description, seq.qual = output
            # seq.update(*output)
            a, b, c, d = output
            seq.update(a, b, c, d)
            yield seq
            output = [i[: -1]]
        else:
            output.append(i[: -1])

    if len(output) == 4:
        #seq.id, seq.seq, seq.description, seq.qual = output
        a, b, c, d = output
        seq.update(a, b, c, d)
        yield seq


code = [0] * 256
flag = 0
for i in 'ATGC':
    code[ord(i.lower())] = code[ord(i)] = flag
    flag += 1

scale = max(code) + 1

# fast convert kmer to number


def k2n(s, scale=4, code=code):
    if scale == -1:
        #scale = code.max() + 1
        scale = max(code) + 1
    n = len(s)
    N = 0
    output = 0
    # for i in s[::-1]:
    for c in xrange(n - 1, -1, -1):
        i = s[c]
        # print 'char', c, i, len(s), code[ord(i)]
        output += code[ord(i)] * int(pow(scale, N))
        #output += code[ord(i)] * pow(scale, N)
        N += 1

    return int(output)


def s2n_next(start, ksize, scale, code, char): return start % int(
    pow(scale, (ksize - 1))) * scale + code[ord(char)]

# convert kmer to number from a seq


def seq2n(s, k=15, scale=4, code=code):
    n = len(s)
    if n <= k:
        yield k2n(s, scale, code)
    else:
        start = k2n(s[0: k], scale, code)
        yield start
        for i in s[k: n]:
            start = s2n_next(start, k, scale, code, i)
            yield start


# kmer count function
def kmc(seq, bucket, ksize, scale):
    for i in seq2n(seq, ksize, scale):
        val = intmask(bucket[i])
        val = val < 65535 and val + 1 or val
        bucket[i] = r_ushort(val)


# count the kmer from the paired fastq file
def fq2c(qry):
    ksize = max(2, int(qry[0]))
    names = qry[1:]
    D = len(names)
    scale = 4
    #buck = [array('H', [0]) * pow(scale, k) for elem in xrange(D // 2)]
    #buck = [array('H', [0]) * scale ** k for elem in xrange(D // 2)]
    #buck = np.zeros((D//2, scale ** k), 'int32')
    N = int(pow(scale, ksize))
    buck = [[r_ushort(0) for elem0 in xrange(N)] for elem1 in xrange(D // 2)]

    print 'ksize, names, D, N, buck shape', ksize, names, D, N, len(
        buck), len(buck[0])

    flag = 0
    itr = 1
    init0 = init1 = time()
    # for name0, name1 in zip(names[0::2], names[1::2]):
    for i in xrange(0, len(names), 2):
        name0, name1 = names[i], names[i + 1]
        print 'qry0', name0, 'qry1', name1
        f0 = open(name0, 'r')
        f1 = open(name1, 'r')
        seqs0 = parse(f0, 'fastq')
        #seqs0 = SeqIO.parse(f0, 'fastq')
        seqs1 = parse(f1, 'fastq')
        #seqs1 = SeqIO.parse(f1, 'fastq')
        for seq0, seq1 in izip([seqs0, seqs1]):
            if seq0.qual.count('N') > 20 or seq1.qual.count('N') > 20:
                continue

            kmc(seq0.seq, buck[flag], ksize, scale)
            kmc(seq1.seq, buck[flag], ksize, scale)

            # timing
            if itr % 1000000 == 0:
                print 'iteration', itr, 'time', time() - init1, 'total time', time() - init0
                init1 = time()
            itr += 1

        f0.close()
        f1.close()

        flag += 1

    # print 'buck', [[intmask(b1) for b1 in b0] for b0 in buck]

    # convert the each reads to a freq hist
    flag = 0
    itr = 1
    init0 = init1 = time()
    # for name0, name1 in zip(names[0::2], names[1::2]):
    for i in xrange(0, len(names), 2):
        name0, name1 = names[i], names[i + 1]
        print 'qry0', name0, 'qry1', name1
        f0 = open(name0, 'r')
        f1 = open(name1, 'r')
        seqs0 = parse(f0, 'fastq')
        #seqs0 = SeqIO.parse(f0, 'fastq')
        seqs1 = parse(f1, 'fastq')
        #seqs1 = SeqIO.parse(f1, 'fastq')
        for seq0, seq1 in izip([seqs0, seqs1]):
            if seq0.qual.count('N') > 20 or seq1.qual.count('N') > 20:
                continue

            output = []
            fwd = [intmask(buck[flag][elem])
                   for elem in seq2n(seq0.seq, ksize, scale, code)]
            rev = [intmask(buck[flag][elem])
                   for elem in seq2n(seq1.seq, ksize, scale, code)]
            med = len(fwd) // 2
            step = 16
            start, end = max(0, med - step), max(0, med + step)
            # for test, only keep positive
            output = fwd[start: end] + rev[start: end]
            #output = fwd[start: end]
            # output.sort()
            TimSort(output).sort()

            if len(output) < step * 2:
                output.extend([0] * (step * 2 - len(output)))

            # print max(output), min(output), mean(output), std(output), output
            #A, B, C, D = khist(output)
            # print ' '.join(map(str, A + ['|', B, C, D]))
            # print ' '.join(map(str, output))
            print 'output', ' '.join([str(out) for out in output])

            # timing
            if itr % 1000000 == 0:
                print 'iteration', itr, 'time', time() - init1, 'total time', time() - init0
                init1 = time()
            itr += 1

        f0.close()
        f1.close()

        flag += 1

    return buck


# the codon usage bias
codons = ['AAA', 'AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG', 'ACT', 'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC', 'ATG', 'ATT', 'CAA', 'CAC', 'CAG', 'CAT', 'CCA', 'CCC', 'CCG', 'CCT', 'CGA', 'CGC', 'CGG', 'CGT', 'CTA', 'CTC', 'CTG',
          'CTT', 'GAA', 'GAC', 'GAG', 'GAT', 'GCA', 'GCC', 'GCG', 'GCT', 'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT', 'TAA', 'TAC', 'TAG', 'TAT', 'TCA', 'TCC', 'TCG', 'TCT', 'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG', 'TTT']
codons_idx = {'ACC': 5, 'ATG': 14, 'AAG': 2, 'AAA': 0, 'ATC': 13, 'AAC': 1, 'ATA': 12, 'AGG': 10, 'CCT': 23, 'CTC': 29, 'AGC': 9, 'ACA': 4, 'AGA': 8, 'CAT': 19, 'AAT': 3, 'ATT': 15, 'CTG': 30, 'CTA': 28, 'ACT': 7, 'CAC': 17, 'ACG': 6, 'CAA': 16, 'AGT': 11, 'CCA': 20, 'CCG': 22, 'CCC': 21, 'TAT': 51, 'GGT': 43, 'TGT': 59, 'CGA': 24, 'CAG': 18, 'CGC': 25,
              'GAT': 35, 'CGG': 26, 'CTT': 31, 'TGC': 57, 'GGG': 42, 'TAG': 50, 'GGA': 40, 'TAA': 48, 'GGC': 41, 'TAC': 49, 'GAG': 34, 'TCG': 54, 'TTA': 60, 'TTT': 63, 'GAC': 33, 'CGT': 27, 'GAA': 32, 'TCA': 52, 'GCA': 36, 'GTA': 44, 'GCC': 37, 'GTC': 45, 'GCG': 38, 'GTG': 46, 'TTC': 61, 'GTT': 47, 'GCT': 39, 'TGA': 56, 'TTG': 62, 'TCC': 53, 'TGG': 58, 'TCT': 55}
syms_idx = {'ACC': 8, 'ATG': 12, 'AAG': 4, 'AAA': 4, 'ATC': 13, 'AAC': 19, 'ATA': 13, 'AGG': 16, 'CCT': 6, 'CTC': 15, 'AGC': 2, 'ACA': 8, 'CTT': 15, 'CAT': 11, 'AAT': 19, 'ATT': 13, 'CTG': 15, 'CTA': 15, 'ACT': 8, 'CAC': 11, 'ACG': 8, 'CCG': 6, 'AGT': 2, 'CAG': 3, 'CAA': 3, 'CCC': 6, 'TAT': 20, 'GGT': 5, 'TGT': 0, 'CGA': 16, 'CCA': 6, 'TCT': 2,
            'GAT': 1, 'CGG': 16, 'TTT': 9, 'TGC': 0, 'GGG': 5, 'TAG': 7, 'GGA': 5, 'TAA': 7, 'GGC': 5, 'TAC': 20, 'TTC': 9, 'TCG': 2, 'TTA': 15, 'AGA': 16, 'GAC': 1, 'TCC': 2, 'GAA': 14, 'TCA': 2, 'GCA': 10, 'GTA': 18, 'GCC': 10, 'GTC': 18, 'GCG': 10, 'GTG': 18, 'GAG': 14, 'GTT': 18, 'GCT': 10, 'TGA': 7, 'TTG': 15, 'CGT': 16, 'TGG': 17, 'CGC': 16}


def codon_bias(s):
    n = len(s)
    nt = [0.] * 64
    aa = [0.] * 21
    for i in xrange(0, n, 3):
        k = s[i: i + 3]
        if k in codons_idx:
            nt[codons_idx[k]] += 1
            aa[syms_idx[k]] += 1
    for k in codons:
        if aa[syms_idx[k]] > 0:
            nt[codons_idx[k]] /= aa[syms_idx[k]]

    return nt


# find the longest orf
stop_codon = ['uaa', 'uag', 'uga', 'taa', 'tag', 'tga']


def longest_orf(s):
    n = len(s)
    start = end = flag = 0
    locus = [[0, 0], [1, 1], [2, 2]]
    for i in xrange(n - 2):
        idx = i % 3
        st, ed = locus[idx][0], i + 3
        if ed - st > flag:
            start, end = st, ed
            flag = ed - st

        if s[i: ed] in stop_codon:
            locus[idx][0] = locus[idx][1] = ed

    return start, end


# reverse complementary of sequence
# waston crick pair
wcp = {'a': 'T', 'A': 'T', 'g': 'C', 'G': 'C',
       't': 'A', 'T': 'A', 'c': 'G', 'C': 'G'}


def rc(s):
    n = len(s)
    return ''.join([wcp.get(s[elem], 'N') for elem in xrange(n - 1, -1, -1)])


# cdf of normal distribution
def ncdf(x): return erfc(-x / 1.4142135623730951) / 2


# the sum, mean and std of an array/list
def sum(x):
    flag = 0
    #a = [[1] * 100 for elem in xrange(pow(10, 6))]
    for i in x:
        flag += i
        # a.append(i)
    return flag


def mean(x): return 1. * sum(x) / len(x)


def std(x):
    if len(x) <= 1:
        return 0
    else:
        m = mean(x)
        var = sum([(elem - m) * (elem - m) for elem in x]) / (len(x) - 1.)
        return sqrt(var)

# dot function
def dot(x, y):
    lx, ly = len(x), len(y)
    n = min(lx, ly)
    d = 0
    for i in xrange(n):
        d += x[i] * y[i]

    return d



# the bfprt
def bfprt(x, k, key=lambda x: x):
    n = len(x)
    for i in xrange(0, n, n // 5):
        insort(x, i, i + n // 5, key)
    y = [x[i] for i in xrange(2, n, n // 5)]
    m = len(y)
    insort(y, 0, m)
    p = y[m // 2]


# ks test for 2 sample
def ks_2samp(x, y):
    lx, ly = len(x) + 0., len(y) + 0.
    D = i = j = 0
    while i < lx and j < ly:
        xi = x[i]
        yj = y[j]
        if xi <= yj:
            i += 1
            fn1 = i / lx
        if yj <= xi:
            j += 1
            fn2 = j / ly
        d = abs(fn1 - fn2)
        if D <= d:
            D = d

    a = 2. / pow(2.71828182846, 2 * D * D * lx * ly / (lx + ly))
    return a


# the ks 2 sample
def ks_statistic(obs_one, obs_two):
    # qsort(obs_one)
    cdf_one = obs_one
    # qsort(obs_two)
    cdf_two = obs_two

    i = 0
    j = 0
    d = 0.
    fn1 = 0.
    fn2 = 0.
    l1 = len(cdf_one) + 0.
    l2 = len(cdf_two) + 0.

    while (i < len(cdf_one) and j < len(cdf_two)):
        d1 = cdf_one[i]
        d2 = cdf_two[j]
        if d1 <= d2:
            i = i + 1
            fn1 = i / l1
        if d2 <= d1:
            j = j + 1
            fn2 = j / l2
        dist = abs(fn2 - fn1)
        if dist > d:
            d = dist

    return d


def ks_significance(alam):
    EPS1 = .001
    EPS2 = 1e-8

    fac = 2.
    flag = 0.
    term_bf = 0.

    a2 = -2. * alam * alam
    for j in xrange(1, 100):
        term = fac * exp(a2 * j * j)
        flag += term
        if abs(term) <= EPS1 * term_bf or abs(term) <= EPS2 * flag:
            # print 'return p value', alam
            return flag
        fac = -fac
        term_bf = abs(term)

    # failing to converge
    return 1.0


"""
  from numerical recipies
"""


def ks_test(obs_one, obs_two):
    d = ks_statistic(obs_one, obs_two)
    # print 'd is', d
    l1 = len(obs_one)
    l2 = len(obs_two)

    en = sqrt(l1 * l2 / (l1 + l2))
    return ks_significance((en + 0.12 + 0.11 / en) * d)  # magic numbers


def ks_test_c(x, y): return 1 - ks_test(x, y)

# rank the sorted data


def rankdata(val):
    n = len(val)
    ts = []
    rank = range(n)
    start = end = 0
    for i in xrange(1, n):
        if val[start] < val[i]:
            if start < end:
                #ri = float(start + end) / (i - start)
                ri = (start + end) / 2.
                ts.append(i - start)
                # print 'hello', ri, i, start
                for j in xrange(start, i):
                    rank[j] = ri

            start = i
        else:
            end = i

    if start < end:
        ri = float(start + end) / 2.
        ts.append(n - start)
        # print 'hello', ri
        for j in xrange(start, n):
            rank[j] = ri

    # correct start from 0
    # for i in xrange(n):
    #    rank[i] += 1

    return rank, ts


# tiecorrect
#tiecorrect = lambda ts, n: ts and 1 - sum([t ** 3. - t for t in ts]) / (n ** 3 - n) or 1
def tiecorrect(ts, n): return ts and 1 - \
    sum([pow(t, 3) - t for t in ts]) / (pow(n, 3) - n) or 1

# Mann–Whitney U test
# return the z score of U
# def mannwhitneyu(x, y, use_continuity = True, alternative = 'two-sided'):


def mannwhitneyu(x, y, use_continuity=False):
    #n0, n1 = map(len, [x, y])
    n0, n1 = len(x), len(y)
    n = n0 + n1
    val = [0] * n
    lab = [0] * n
    p0 = p1 = p2 = 0
    while p0 < n0 and p1 < n1:
        if x[p0] < y[p1]:
            val[p2] = x[p0]
            lab[p2] = 0
            p0 += 1
            p2 += 1

        elif x[p0] > y[p1]:
            val[p2] = y[p1]
            lab[p2] = 1
            p1 += 1
            p2 += 1

        else:
            val[p2] = x[p0]
            lab[p2] = 0
            p0 += 1
            p2 += 1

            val[p2] = y[p1]
            lab[p2] = 1
            p1 += 1
            p2 += 1

    while p0 < n0:
        val[p2] = x[p0]
        lab[p2] = 0
        p0 += 1
        p2 += 1

    while p1 < n1:
        val[p2] = y[p1]
        lab[p2] = 1
        p1 += 1
        p2 += 1

    # correct the tie rank
    # tied rank
    rank, ts = rankdata(val)
    #rank0 = sum([a for a, b in izip(rank, lab) if b == 0])
    # add n0 to correct the start from 0
    #Rank0 = [a for a, b in izip(rank, lab) if b == 0]
    Rank0 = [rank[i] for i in xrange(n) if lab[i] == 0]
    rank0 = sum(Rank0) + n0

    u0 = n0 * n1 + n0 * (n0 + 1) / 2. - rank0
    #u1 = n1 + sum([a for a, b in zip(rank, lab) if b == 1]) - n1 * (n1 + 1) / 2
    u1 = n0 * n1 - u0

    u = min(u0, u1)
    mu = n0 * n1 / 2.
    var = n0 * n1 * (n + 1) * tiecorrect(ts, n) / 12.
    #sd = var ** .5
    sd = pow(var, .5)
    z = use_continuity and (abs(u - mu) - .5) / sd or abs(u - mu) / sd

    if z >= 0:
        p = 2 - 2 * ncdf(z)
    else:
        p = 2 * ncdf(z)

    return u, p


# comp of mann
#mannwhitneyu_c = lambda x, y: 1 - mannwhitneyu([intmask(elem) for elem in x], [intmask(elem) for elem in y])[1]
def mannwhitneyu_c(x, y): return 1 - mannwhitneyu(x, y)[1]




def normalize(x, unit=True):
    u = mean(x)
    if unit:
        v = sum([(elem-u)*(elem-u) for elem in x])
        s = sqrt(abs(v))
        s = s > 0 and s or s + 1e-9
    else:
        s = std(x)
    return [(elem-u)/s for elem in x]

# unit a vector x
def unit(x):
    v = sum([elem*elem for elem in x])
    s = sqrt(abs(v))
    #s = std(x)
    return [elem/s for elem in x]




# the euclidean distance
def euclidean(x, y):
    lx = len(x)
    ly = len(y)
    n = min(lx, ly)

    d = 0
    for i in xrange(n):
        z = (x[i] - y[i])
        d += z * z

    return sqrt(abs(d))


def euclidean_norm(x, y):
    x_m = mean(x)
    x_sd = std(x)
    X = [(elem-x_m)/x_sd for elem in x]

    y_m = mean(y)
    y_sd = std(y)
    Y = [(elem-y_m)/y_sd for elem in y]
    #Z = euclidean(X, Y)
    d = 0.
    for i in xrange(len(X)):
        z = (X[i] - Y[i])
        d += z * z
    return d


# dist between x and y
# the dist can be normalized by the norm of x or y
def dist(x, y, norm=True):
    nx, ny, nz = [sqrt(elem) for elem in map(sum, [[xi * xi for xi in x],
                                                   [yi * yi for yi in y], [(yi - xi) * (yi - xi) for xi, yi in zip(x, y)]])]
    return norm and nz / nx or nz / ny


# the pearson relationship
def pearson(x, y):
    lx, ly = len(x), len(y)
    N = min(lx, ly)
    #assert N == M
    x_m, y_m = mean(x), mean(y)
    a = b = c = 0.
    #N = lx < ly and lx or ly

    for i in xrange(N):
        xi, yi = x[i] - x_m, y[i] - y_m
        a += xi * yi
        b += xi * xi
        c += yi * yi

    d2 = b * c
    d = sqrt(abs(d2))
    if d > 0:
        return a / d
    else:
        return b == c and 1. or 0.


# convert pearson to dist
def p2d(p, n):
    d = 2 * n * (1-p)
    return sqrt(d)


def d2p(d, n):
    p = 1 - d * d / 2. / n
    return p


# pearson dist
def pdist(x, y, dim=-1):
    if dim < 0:
        lx = len(x)
    else:
        lx = dim
    p = pearson(x, y)
    #print 'p is', p
    d2 = 2 * lx * abs(1-p)
    #print 'd2 is', d2
    d = sqrt(d2)
    return d


# pearson for sparse
def pearson_sp(x0, x1):
    y0, z0 = x0
    y1, z1 = x1
    #l0 = len(y0)
    #n = y0[l0-1]
    n = y0[-1]
    #print 'length is', n
    l0 = len(y0) - 1
    l1 = len(y1) - 1
    if l0 <= 0 or l1 <= 0:
        pr = 0
    else:
        p0 = p1 = 0
        xy = 0.
        # while p0 < l0 and p1 < l1:
        for idx in xrange(l0+l1):
            if p0 >= l0 or p1 >= l1:
                break
            a, b = y0[p0], y1[p1]
            if a == b:
                xy += z0[p0] * z1[p1]
                p0 += 1
                p1 += 1
            elif a < b:
                p0 += 1
            else:
                p1 += 1

        z0_s, z1_s = sum(z0), sum(z1)
        #z0_s = 0
        # for elem in z0:
        #    z0_s += elem

        #z1_s = 0
        # for elem in z1:
        #    z1_s += elem

        z0_sq_s = sum([elem*elem for elem in z0])
        #z0_sq_s = 0
        # for elem in z0:
        #    z0_sq_s += elem * elem

        z1_sq_s = sum([elem*elem for elem in z1])
        #z1_sq_s = 0
        # for elem in z1:
        #    z1_sq_s += elem * elem

        A = n * xy - z0_s * z1_s
        B = (n * z0_sq_s - z0_s * z0_s) * (n * z1_sq_s - z1_s*z1_s)
        B = sqrt(abs(B))
        c = B > 0 and A / B or 0
        pr = c

    return pr


def pdist_sp(x, y):
    p = pearson_sp(x, y)
    #print 'p is', p
    l = len(x[0])
    n = x[0][l-1]
    d2 = 2 * n * abs(1-p)
    #print 'd2 is', d2
    d = sqrt(d2)
    return d


def get_row(x, start=0, sep=','):
    j = x[:-1].split(sep)
    n = len(j)
    #flag = 0
    #ys, zs = [], []
    zs = []
    for i in xrange(start, n):
        try:
            z = float(j[i])
        except:
            z = 0
        zs.append(z)
        #flag += 1

    # ys.append(int(flag))
    # zs.append(0)
    return zs


# get sparse array
def get_row_sp(x, start=0, sep=','):
    j = x[:-1].split(sep)
    n = len(j)
    ys, zs = [], []
    #flag = 0
    for i in xrange(start, n):
        try:
            z = float(j[i])
        except:
            z = 0
        if z > 0:
            ys.append(i-start)
            zs.append(z)

        #print 'before flag', flag, i-start
        #flag += 1
        #print 'after flag', flag, i-start

    #flag = 0
    # for i in xrange(start, n):
    #    flag += 1

    #print 'row length', flag, start, n
    ys.append(n - start)
    zs.append(0)
    return [ys, zs]


# update centroid
def acentroid(cx, x, cy, y): return [
    cx * x[elem] + cy * y[elem] for elem in xrange(len(x))]
# find the centroid


def centroid(X, L=[]):
    if len(L) == 0:
        L = range(len(X))

    N = len(L)
    x = X[L[0]]
    n = 1
    for i in xrange(N):
        y = X[L[i]]
        n += 1
        cy = 1. / n
        cx = 1 - cy
        acentroid(cx, x, cy, y)

    return x

# online kmean


def kmean(X, eps=.8, itr=25):
    # C store the cenoid
    #Cs = X[::len(X)//30]
    Cs = X[:30]
    # N stroe the count of each cenoid
    Ns = [1] * 30
    for i in xrange(itr):
        for x in X:
            if Cs:
                P, idx, y = 0, -1, x
                #P, idx = 0, -1
                for j in xrange(len(Cs)):
                    v = Cs[j]
                    u, p = mannwhitneyu(x, v)
                    if eps < p > P:
                        P, idx, y = p, j, v

                if idx == -1:
                    # Cs.append(x)
                    # Ns.append(1)
                    continue
                else:
                    print 'adjust centroid'
                    N = Ns[idx]
                    cy = 1. / (N + 1)
                    cx = 1 - cy
                    Cs[idx] = acentroid(cx, x, cy, y)
                    Ns[idx] += 1
            else:
                Cs.append(x)
                Ns.append(1)

            # print 'Number of cluster', len(Cs)
    # print 'size of Cs', len(Cs)
    flag = 0
    for x in X:
        for y in Cs:
            u, p = mannwhitneyu(x, y)
            if p > eps:
                flag += 1
                break
    print 'classifiled point', flag
    return Cs
    # return flag


# DBScan algorithm
def regionQuery(p, D, eps):
    n = len(D)
    P = D[p]
    neighbor = []
    for i in xrange(n):
        u, p = mannwhitneyu(P, D[i])
        if p <= eps:
            neighbor.append(i)

    return neighbor


def expandCluster0(i, NeighborPts, D, Dtree, L, C, eps, MinPts):

    L[i] = C
    unvisit = [elem for elem in NeighborPts]
    visit = {}
    while len(unvisit) > 0:
        j = unvisit.pop()
        if j not in visit:
            visit[j] = 0
        else:
            continue
        #j = unvisit.popleft().val
        if len(D) <= 50000:
            jNeighborPts = regionQuery(j, D, eps)
        else:
            jNeighborPts = Dtree.query_radius(D[j], eps)
        if len(jNeighborPts) > MinPts:
            new = [elem for elem in jNeighborPts]
            unvisit.extend(new)
        if L[j] < 1:
            L[j] = C


def expandCluster(i, NeighborPts, D, Dtree, L, C, eps, MinPts, fast=True):

    L[i] = C
    unvisit = [elem for elem in NeighborPts if L[elem] == 0]
    #unvisit = llist([elem for elem in NeighborPts if L[elem] == 0])
    for j in NeighborPts:
        L[j] = C

    # while unvisit:
    while len(unvisit) > 0:
        j = unvisit.pop()
        if L[j] < 1:
            L[j] = C
        #j = unvisit.popleft().val
        if fast:
            jNeighborPts = Dtree.query_radius(D[j], eps)
        else:
            jNeighborPts = regionQuery(j, D, eps)

        if len(jNeighborPts) > MinPts:
            new = [elem for elem in jNeighborPts if L[elem] == 0]
            unvisit.extend(new)
            for k in new:
                L[k] = C

    # print 'set all C', C, i, flag, len(f_dict)
    # gc.collect()


# < 0: noise
# = 0: unclassified, unvisitied
# > 0: classified
# def dbscan(D, eps = 1e-3, MinPts = 10, dist = mannwhitneyu_c, fast = True):
def dbscan(D, eps=1e-3, MinPts=10, dist=ks_test_c, fast=True):

    Dtree = Cvt(D)
    if fast:
        Dtree.fit()
    n = len(D)
    C = 0
    # label to record the type of point
    L = [0] * n
    t0 = time()
    for i in xrange(n):
        if i % 10000 == 0:
            # print 'iteration', i, time() - t0
            t0 = time()

        # if point i is visited, then pass
        if L[i] != 0:
            continue

        if len(D) < 50000:
            NeighborPts = regionQuery(i, D, eps)
        else:
            NeighborPts = Dtree.query_radius(D[i], eps)
        # print 'Neighbor Pts size is', len(NeighborPts), i, eps
        if len(NeighborPts) < MinPts:
            # print 'add noise'
            L[i] = -1
        else:
            # print 'before C', C, i
            C += 1
            # print 'after C', C, i
            # print 'extension cluster', C
            expandCluster(i, NeighborPts, D, Dtree, L, C, eps, MinPts)

    fq = {}
    for i in L:
        try:
            fq[i] += 1
        except:
            fq[i] = 1

    # for i in fq:
    #    print 'cluster', i, fq[i]
    print 'end L', Max(L)
    return L


# the canopy algoithm
# for euc, t1 > t2
# for cor, t1 < t2
# def canopy(data, t1 = 2., t2 = 1.5, dist = pearson):
def canopy(data, t1=.4, t2=.2, dist=mannwhitneyu_c):
    # def canopy(data, t1 = 0, t2 = 1e-3, dist = pearson):

    canopies = []
    _o = open('canopy.npy', 'w')
    idxs = range(len(data))
    #idxs =  array('i')
    # for i in xrange(len(data)):
    #    idxs.append(i)

    # shuffle the index
    # shuffle(idxs)

    # the can and keep array
    init0_time = time()
    init1_time = time()
    flag = 0
    while idxs:
        idx = idxs.pop()
        #x = [intmask(int(val)) for val in data[idx]]
        x = map(intmask, data[idx])

        can = [idx]
        #can = array('i', [idx])
        #del can[:]
        # can.append(idx)

        keep = []
        #keep = array('i')
        #del keep[:]

        if dist == mannwhitneyu:
            print 'mann'
            for elem in idxs:
                # while idxs:
                #elem = idxs.pop()
                #y = [intmask(val) for val in data[elem]]
                y = map(intmask, data[elem])
                u, p = dist(x, y)
                if p > t1:
                    can.append(elem)
                if p < t2:
                    keep.append(elem)
                # print 'size', len(idxs)

        elif dist == pearson:
            print 'pearson'
            for elem in idxs:
                # while idxs:
                #elem = idxs.pop()
                #y = [intmask(val) for val in data[elem]]
                y = map(intmask, data[elem])
                cor = dist(x, y)
                if cor > t1:
                    can.append(elem)
                if cor < t2:
                    keep.append(elem)
                # print 'size', len(idxs)

        else:
            print 'mann_c'
            for elem in idxs:
                # while idxs:
                #elem = idxs.pop()
                #y = [intmask(val) for val in data[elem]]
                y = map(intmask, data[elem])

                d = dist(x, y)
                if d < t1:
                    can.append(elem)
                if d > t2:
                    keep.append(elem)
            print 'reduce point', len(idxs) - len(keep)

        # use -1 as sep and save to disk
        can.append(-1)
        canopies.extend(can)
        if len(canopies) >= 1000000:
            string = ''.join([pack('i', elem) for elem in canopies])
            _o.write(string)
            canopies = []
        # canopies.write(string)
        # print 'can size', len(can), len(keep)
        # print 'can size', len(can), 'reduce', len(idxs) - len(keep), len(canopies)
        #del x, can, idxs
        idxs = keep
        #del keep
        gc.collect()
        print 'use time', time() - init1_time, 'total', time() - init0_time
        init1_time = time()

    if len(canopies) > 0:
        string = ''.join([pack('i', elem) for elem in canopies])
        _o.write(string)
        canopies = []

    # canopies.close()
    return canopies


# the disk base array
class array:

    def __init__(self, fn, dtype='i', mode='r+', shape=()):

        self.fn = fn
        self.dtype = dtype
        self.mode = mode
        #self.shape = shape
        if self.dtype == 'i':
            self.stride = 4
        else:
            self.stride = 2

        if self.mode == 'r+':
            f = open(self.fn, 'rb', 1024*1024*256)
            ACCESS = rmmap.ACCESS_READ
        elif mode == 'w+' and shape != ():
            # create the file
            _o = open(self.fn, 'wb', 1024*1024*256)
            ACCESS = rmmap.ACCESS_WRITE
            N = self.stride
            for i in shape:
                N *= i
            _o.seek(N-self.stride)
            _o.write('\0'*self.stride)
            _o.close()
            f = open(fn, 'wb', 1024*1024*256)
        else:
            # pass
            f = open(self.fn, 'rb', 1024*1024*256)
            ACCESS = rmmap.ACCESS_READ

        self.f = f
        self.data = rmmap.mmap(self.f.fileno(), 0, access=ACCESS)
        self.N = self.data.size // self.stride
        if mode == 'r+' and shape == ():
            self.shape = (self.N)
        else:
            self.shape = shape

    def __len__(self):
        # return self.N
        return self.shape[0]

    def __getitem__(self, i):
        j = self.data.getslice(i*self.stride, self.stride)
        v = unpack(self.dtype, j)
        return v

    def __getslice__(self, i, j):
        return [self.__getitem__(elem) for elem in xrange(i, j)]

    def __setitem__(self, i, v):
        j = pack(self.dtype, v)
        self.data.setslice(i*self.stride, j)

    def __setitem__(self, i, v):
        pass

    def __flush__(self):
        self.f.flush()

    def close(self):
        self.f.close()



def proju(u, v):
    lu, lv = len(u), len(v)
    n = min(lu, lv)
    d0 = d1 = 1e-9
    for i in xrange(n):
        d0 += u[i] * v[i]
        d1 += u[i] * u[i]

    d = d0 / d1
    return [elem * d for elem in u]


# binary child node
class vertex:
    def __init__(self, hpl, value=[], rad=1000000000, srt=False):
        self.hpl = hpl
        #self.left = [] 
        #self.right = []
        self.left = None
        self.right = None
        self.value = value
        self.rad = rad
        self.n = len(self.value)
        self.srt = srt



# random projection tree or vantage point tree
class RPT:

    def __init__(self, data, eps=1e-6, dist=euclidean, chk=256, norm=normalize):
        self.data, self.eps, self.dist, self.chk, self.norm = data, eps, dist, chk, norm
        self.R = len(data)
        assert self.R > 0
        print 'tree inital', len(data)
        self.C = len(data[0])
        assert self.C > 0

        self.cnt = 0
        val = range(self.R)
        x = self.data[0]
        #if self.norm:
        #    x = normalize(x)
        x = self.norm(x)
        print 'generate hyperplane'
        hpl = self.hyperplane(x)
        #print 'get root', x, hpl
        ds, dmx = self.find_max_dist(hpl, val)
        self.root = vertex(hpl, value=val, rad=dmx)

        # count the number of hyperplane
        #self.u = None

    def find_max_dist(self, x, vals):
        dmx = -10000000000000
        ds = []
        #x = self.data[i]
        for i in vals:
            y = self.data[i]
            d = self.p2h(x, y)
            dmx = max(dmx, d)
            ds.append(d)

        return ds, dmx


    # generate hyperplane
    def hyperplane0(self, v):
        #flag = 0
        #hpl = []
        #n = len(v)
        #for i in xrange(n):
        #    j = i % 2 and -v[i] or v[i]
        #    hpl.append(j)
        #    flag += j
        #hpl.append(0-flag)
        #v = normalize(x)

        n = len(v)
        y = v[-1]
        hpl = [random() for elem in xrange(n-1)]
        S = sum([v[elem]*hpl[elem] for elem in xrange(n-1)])
        hpl.append(-S/y)

        #self.u = hpl

        #if self.cnt % self.C != 0 and self.cnt > 0:
        #    hpl = proju(self.u, hpl)

        hpl = unit(hpl)
        self.u = hpl
        self.cnt += 1

        return hpl

    def hyperplane(self, x):
        #hpl = normalize([random() for elem in xrange(len(x))])
        #return hpl
        return x
        #return self.data[x]


    # build the tree
    def fit0(self):
        stack = [self.root]
        while stack:
            n = stack.pop()
            print 'poping', n
            if len(n.value) < self.chk:
                print 'continue'
                continue
            else:
                n_l, n_r = self.split(n)
                print 'finish split2'
                n.left = n_l
                n.right = n_r
                #stack.extend([n_l, n_r])
                #n.left.append(n_l)
                #n.right.append(n_r)
                if n_l:
                    stack.append(n_l)
                if n_r:
                    stack.append(n_r)

                print 'finish split3'
        print 'finish fit'


    # build the tree
    def fit(self):
        stack = [self.root]
        while stack:
            n = stack.pop()
            print 'poping', n
            if len(n.value) < self.chk:
                print 'continue'
                continue
            else:
                n_l, n_r = self.split(n)
                print 'finish split2'
                n.left = n_l
                n.right = n_r
                #if n_l:
                #    stack.append(n_l)
                #if n_r:
                #    stack.append(n_r)
                if n_l and n_r:
                    stack.extend([n_l, n_r])

                print 'finish split3'
        print 'finish fit'




    # distance from pointer to hyperplane 
    def p2h0(self, p, h):
        n = min(len(p), len(h))
        d = 0
        v2 = 0
        for i in xrange(n):
            d += p[i] * h[i]
            v2 += h[i] * h[i]
        v2 = abs(v2)
        v = sqrt(v2)
        print 'norm_of_hyper', v
        return v > 0 and d / v or d / (v+1e-9)
        #if v <= 0:
            #print 'd v is', d, v, n
            #return d == 0 and 1 or 1e9
        #else:
        #    return d / v


    # distance from pointer to hyperplane 
    def p2h(self, p, h):
        return euclidean(p, h)

    # split the vertex
    def split0(self, node):
        lv, rv = [], []
        while node.value:
            i = node.value.pop()
            x = self.data[i]
            #if self.norm:
            #    x = normalize(x)
            x = self.norm(x)
            if self.p2h(x, node.hpl) < 0:
                lv.append(i)
            else:
                rv.append(i)

        print 'l and r child', len(lv), len(rv)
        if lv:
            x_l = self.data[lv[0]]
            #if self.norm:
            #    x_l = normalize(x_l)
            x_l = self.norm(x_l)
            hpl = self.hyperplane(x_l)
            n_l = vertex(hpl, value=lv)
        else:
            n_l = None
        if rv:
            x_r = self.data[rv[0]]
            #x_r = normalize(x_r)
            x_r = self.norm(x_r)
            hpl = self.hyperplane(x_r)
            n_r = vertex(hpl, value=rv)
        else:
            n_r = None
        print 'finish split'
        return n_l, n_r


    def split(self, node):
        #return node, node
        lv, rv = [], []
        dists, dmx = self.find_max_dist(node.hpl, node.value)
        qsort(dists)
        ld = len(dists)
        #thres = dists[int(ld*.05)]
        thres = dists[ld//2]
        #thres = sqrt(2*(1-.2))
        #thres = .1

        while node.value:
            i = node.value.pop()
            x = self.data[i]
            #if self.norm:
            #    x = normalize(x)
            x = self.norm(x)
            dxh = self.p2h(x, node.hpl)
            #print 'dxh', dxh
            if dxh <= thres:
                lv.append(i)
            else:
                rv.append(i)

        print 'l and r child', len(lv), len(rv), thres
        if lv:
            #x_l = self.data[lv[0]]
            #if self.norm:
            #    x_l = normalize(x_l)
            #x_l = self.norm(x_l)
            #hpl = self.hyperplane(lv[0])
            hpl = self.data[lv[0]]
            dists, dmx = self.find_max_dist(hpl, lv)
            n_l = vertex(hpl, value=lv, rad=dmx)
        else:
            n_l = None
        if rv:
            #x_r = self.data[rv[0]]
            #x_r = normalize(x_r)
            #x_r = self.norm(x_r)
            #hpl = self.hyperplane(rv[0])
            hpl = self.data[rv[0]]
            dists, dmx = self.find_max_dist(hpl, rv)
            n_r = vertex(hpl, value=rv, rad=dmx)
        else:
            n_r = None
        print 'finish split'
        return n_l, n_r



    # get leaf
    def leaf(self, node):
        #if not node:
        #    return []
        #return []
        leaves = []
        stack = [node]
        while stack:
            n = stack.pop()
            n_l, n_r = n.left, n.right
            if n_l:
                stack.append(n_l)
            #else:
            #    leaves.append(n.value)
            if n_r:
                stack.append(n_r)
            #else:
            #    leaves.append(n.value)
            if not n_l and not n_r:
                leaves.extend(n.value)
        return leaves


    def query0(self, x, rad=0):
        #if self.norm:
        #    q = normalize(x)
        #else:
        #    q = x
        q = self.norm(x)
        stack = [self.root]
        output = []
        print 'start query'
        while stack:
            node= stack.pop()
            d = self.p2h(q, node.hpl)
            #d = abs(d)
            print 'curret d', d, rad
            if d <= -rad < 0:
                print 'add left', node.n
                n_l = node.left
                if n_l:
                    stack.append(n_l)
                else:
                    output.extend(node.value)

            elif 0 <= rad <= d:
                print 'add right', d, rad, node.right
                n_r = node.right
                if n_r:
                    print 'right value', n_r.n
                    stack.append(n_r)
                else:
                    output.extend(node.value)
            else:
                print 'add both 0', d, rad, node
                n_l, n_r = node.left, node.right
                print 'add both 1', d, rad, n_l, n_r
                if n_l:
                    stack.append(n_l)
                if n_r:
                    stack.append(n_r)
                if not n_l and not n_r:
                    output.extend(node.value)

        #return output
        out = []
        for elem in output:
            y = self.data[elem]
            #if self.norm:
            #    y = normalize(y)
            y = self.norm(y)
            #if self.dist(q, y) <= rad:
            #    out.append(elem)
            D = self.dist(q, y)
            if D <= rad:
                out.append([elem, D])

        print 'output length', len(output)
        return out 


    def query(self, x, rad=0):
        #return []
        #if self.norm:
        #    q = normalize(x)
        #else:
        #    q = x
        q = self.norm(x)
        stack = [self.root]
        output = []
        print 'start query xx'
        while stack:
            node= stack.pop()
            d = self.p2h(q, node.hpl)
            #d = abs(d)
            print 'curret d', d, node.rad, rad, 'end'
            if d + node.rad <= rad:
                leaves = self.leaf(node)
                #leaves = []
                output.extend(leaves)

            elif d <= rad + node.rad:
                n_l, n_r = node.left, node.right
                if n_l:
                    stack.append(n_l)
                if n_r:
                    stack.append(n_r)
                if not n_l and not n_r:
                    output.extend(node.value)
            else:
                continue
        #return output
        out = []
        for elem in output:
            y = self.data[elem]
            #if self.norm:
            #    y = normalize(y)
            y = self.norm(y)
            #if self.dist(q, y) <= rad:
            #    out.append(elem)
            D = self.dist(q, y)
            if D <= rad:
                out.append([elem, D])

        print 'output length', len(output)
        return out 



# VPT tree
class VP:

    def __init__(self, data, eps=1e-6, dist=euclidean, chk=256, norm=normalize):
        self.data, self.eps, self.dist, self.chk, self.norm = data, eps, dist, chk, norm
        self.R = len(data)
        assert self.R > 0
        print 'vp tree inital', len(data)
        self.C = len(data[0])
        assert self.C > 0

        self.cnt = 0
        val = range(self.R)
        x = self.data[0]
        #if self.norm:
        #    x = normalize(x)
        vp = self.norm(x)
        print 'vp generate hyperplane'
        ds, dmx = self.find_max_dist(vp, val)
        self.root = vertex(vp, value=val, rad=dmx)

        # count the number of hyperplane
        #self.u = None

    def find_max_dist(self, x, vals):
        dmx = -10000000000000
        ds = []
        #x = self.data[i]
        for i in vals:
            y = self.data[i]
            d = self.p2h(x, y)
            dmx = max(dmx, d)
            ds.append(d)

        return ds, dmx


    # build the tree
    def fit(self):
        stack = [self.root]
        while stack:
            n = stack.pop()
            print 'vp poping', n
            if len(n.value) < self.chk:
                print 'continue'
                continue
            else:
                n_l, n_r = self.split(n)
                print 'vp finish split2'
                n.left = n_l
                n.right = n_r
                if n_l and n_r:
                    stack.extend([n_l, n_r])

                print 'vp finish split3'
        print 'vp finish fit'


    # distance from pointer to hyperplane 
    def p2h(self, p, h):
        return euclidean(p, h)


    def split(self, node):
        #return node, node
        lv, rv = [], []
        dists, dmx = self.find_max_dist(node.hpl, node.value)
        qsort(dists)
        ld = len(dists)
        thres = dists[int(ld*.05)]
        #thres = dists[ld//2]
        node.rad = min(thres, node.rad)

        # check wether the point can be split
        L = R = 0
        for d in dists:
            if d <= thres:
                L += 1
            else:
                R += 1
        if L == 0 or R == 0:
            return None, None

        print 'L', L, 'R', R
        while node.value:
            i = node.value.pop()
            x = self.data[i]
            x = self.norm(x)
            dxh = self.p2h(x, node.hpl)
            if dxh <= thres:
                lv.append(i)
            else:
                rv.append(i)

        vp = self.data[lv[0]]
        n_l = vertex(vp, value=lv)
        vp = self.data[rv[0]]
        n_r = vertex(vp, value=rv)
        return n_l, n_r


    # get leaf
    def leaf(self, node):
        #if not node:
        #    return []
        #return []
        leaves = []
        stack = [node]
        while stack:
            n = stack.pop()
            n_l, n_r = n.left, n.right
            if n_l:
                stack.append(n_l)
            #else:
            #    leaves.append(n.value)
            if n_r:
                stack.append(n_r)
            #else:
            #    leaves.append(n.value)
            if not n_l and not n_r:
                leaves.extend(n.value)
        return leaves

    # full == false: only keep half matrix
    def query(self, x, rad=0, full=False):
        #return []
        #if self.norm:
        #    q = normalize(x)
        #else:
        #    q = x
        q = self.norm(x)
        stack = [self.root]
        output = []
        print 'start query the vp'
        while stack:
            node= stack.pop()
            d = self.p2h(q, node.hpl)
            #d = abs(d)
            #print 'curret d', d, node.rad, rad, 'end'
            if d - rad <= node.rad:
                #print  'search left', d, rad, node.rad
                if node.left:
                    stack.append(node.left)
                else:
                    output.extend(node.value)
            if d + rad >= node.rad:
                #print 'search right', d, rad, node.rad
                if node.right:
                    stack.append(node.right)
                else:
                    output.extend(node.value)

        #return output
        out = []
        for elem in output:
            y = self.data[elem]
            #if self.norm:
            #    y = normalize(y)
            y = self.norm(y)
            #if self.dist(q, y) <= rad:
            #    out.append(elem)
            if full == False and q[0] > y[0]:
                continue

            D = self.dist(q, y)
            if D <= rad:
                out.append([elem, D])

        print 'output length', len(output), len(out)
        return out 




# multiple child node
class Node:
    #def __init__(self, key, rank, level = 0, radius = 1):
    def __init__(self, key, rank, num=0, radius=1):
        self.key = key
        self.rank = rank
        self.num = num
        #self.level = level
        self.radius = radius
        self.child = []


# cover tree
class Cvt:

    def __init__(self, data, eps=1e-8, dist=ks_test_c, chk=128):

        self.data = data
        self.eps = eps
        self.scale = .8
        self.rate = .8
        self.dist = dist
        self.chk = chk
        radius = -1
        n = len(data)
        #flag = 0
        x = 0
        dists = []
        #print data[0]
        #print data[1437]
        for y in xrange(1, n):
            current = self.dist(data[x], data[y])
            #print 'current_xy_dist', current, x, y, euclidean(data[0], data[1437]), len(data[0]), len(data[1437])
            #radius = radius < current and current or radius
            radius = current if radius < current else radius
            #flag += current > .2
            #flag += current < 42
            #print 'dist', current, x, y, pearson(data[x], data[y])
            dists.append(current)

        qsort(dists)
        ld = len(dists)
        self.scale = dists[int(ld * self.rate)] / radius
        #print 'current radius is', radius, 'flag', flag, self.scale
        print 'current radius is', radius, self.scale, 'min dists', dists[0], 'max dists', dists[-1]
        #print 'all_dist', dists
        self.root = Node(0, range(n), n, radius)
        print 'Node_rank0', len(self.root.rank), 'start_root', len(self.root.rank)

        # print 'at least half', flag, self.scale
        #self.radius = radius
        #self.maxlevel = radius > 0 and int(log(radius, 2) + 1) or 1
        #self.maxlevel = log(12, 2)

    # reduce the radius
    def rd_radius(self, rank, radius):
        if len(rank) <= 1:
            return 0, 0

        data =self.data
        x = rank[0]
        dists = [self.dist(data[x], data[y]) for y in rank[1:]]
        ld = len(dists)

        if ld > 1:
            qsort(dists)

        #print 'reduced radius is', radius, self.scale, 'min dists', dists[0], 'max dists', dists[-1]

        left = int(ld * self.rate)
        rad = dists[left]
        rad = rad < radius and rad or radius * self.rate
        right = (ld - left) // 2 + left
        rad2 = dists[right]
        #return rad, rad2
        #print 'rad2 is', rad2
        return rad, rad2
        


    def fit(self):

        nodes = [self.root]
        #print 'root_fit', len(self.root.rank)
        #scale = self.scale
        while nodes:
            n0 = nodes.pop()
            #print 'node', n0, 'poped'
            #level = n0.level + 1
            #radius = self.radiu * pow(scale, level)
            #cutoff = n0.radius * pow(scale, level)

            # if cutoff > self.eps and len(n0.rank) > 1:
            if n0.num <= self.chk:
                continue

            elif n0.radius > self.eps and len(n0.rank) > 1:
            #if n0.radius > self.eps and len(n0.rank) > 1:

                #cutoff = n0.radius * self.scale
                #cutoff = self.rd_radius(n0.rank, n0.radius)
                cutoff, cutoff2 = self.rd_radius(n0.rank, n0.radius)
                # if n0.key == 0:
                #    print 'first node', radius, len(n0.rank)

                radius = flag = 0
                # print 'first x data', n0.key
                #for (radius, rank) in self.split(n0.rank, cutoff):
                for (radius, rank) in self.split(n0.rank, cutoff, cutoff2):
                    #print 'split set size', len(rank), radius, cutoff, n0.key
                    #print 'split set size', len(rank), radius, cutoff, cutoff2, n0.key
                    #print 'split set size', len(rank), 'level', level, 'radius', radius, 'self radius', self.radius
                    #n1 = Node(rank[0], rank, level, radius)
                    # if radius < 0:
                    #    continue
                    n1 = Node(rank[0], rank, len(rank), radius)
                    #print 'Node_rank1', len(n1.rank)
                    n0.child.append(n1)
                    nodes.append(n1)
                    flag += 1

                #print 'found nn', flag, radius, len(n0.rank)
            elif n0.radius > self.eps and len(n0.rank) <= 1:
                #print 'debug test'
                n0.radius = 0
                # print 'split', flag, 'child length', len(n0.child)

            # elif n0.radius <= self.eps:
            #    data = self.data
            #    if n0.key == len(data) // 2:
            # print 'very small point', len(n0.rank),
            # Max([mannwhitneyu_c(data[n0.rank[0]], data[elem]) for elem in
            # n0.rank]), len(n0.child)
            else:
                # if len(n0.child) == 1:
                #    print 'not split', n0.key, n0.child[0].key
                # elif len(n0.child) == 0:
                #    print 'not split 2', n0.key, n0.radius
                continue

    # setup root
    def split(self, rank, cutoff, cutoff2=-1):
        rank[0], rank[-1] = rank[-1], rank[0]
        data = self.data
        cut_max = -1
        while rank:
            #radius = -1
            radius = 0
            x = rank.pop()
            inner, outer = [x], []
            cut2_idx = -1
            while rank:
                y = rank.pop()
                current = self.dist(data[x], data[y])
                if current <= cutoff:
                    #print 'current dist', x, y, current, cutoff
                    #radius = radius < current and current or radius
                    radius = current if radius < current else radius
                    # if radius == -1:
                    # print 'radius', radius, 'current longest', current,
                    # 'change', radius < current

                    inner.append(y)
                else:
                    outer.append(y)
                    if y > cut_max:
                        cut_max = y
                        cut2_idx = len(outer) - 1

                # print 'current radius is', radius, current
            if  0 <= cut2_idx < len(outer) - 1:
                outer[cut2_idx], outer[-1] = outer[-1], outer[cut2_idx]
            #print 'inner set size', len(inner), 'outer', len(outer)
            # if radius == -1:
            # print 'error radius', cutoff, [mannwhitneyu_c(data[inner[0]],
            # data[elem]) for elem in inner]
            yield radius, inner
            rank = outer
            #print 'after yield', len(rank)

    # dfs get all leaves's data by give an inner node
    def leaf(self, n):
        nodes = [n]
        #visit = {}
        ranks = []
        while nodes:
            node = nodes.pop()
            #if node.key not in visit:
            #    visit[node.key] = 1
            #else:
            #    continue
            if node.child:
                nodes.extend(node.child)

            #ranks.extend(node.rank)
            else:
                ranks.extend(node.rank)
                #for i in node.rank:
                #    visit[i] = 1

        #ranks = visit.values()
        return ranks
        #return visit

    # for debug
    def root_leaf(self):
        p = self.root
        while len(p.child) > 0:
            p = [elem for elem in p.child if elem.key == 0][0]

        # return p.rank, p.level, self.radius * pow(self.scale, p.level)
        flag = 0
        for i in p.rank:
            # if mannwhitneyu_c(self.data[0], self.data[i]) > self.radius *
            # pow(self.scale, p.level):
            if mannwhitneyu_c(self.data[0], self.data[i]) > p.radius:
                flag += 1
        # return flag, self.radius * pow(self.scale, p.level)
        return flag, p.radius

    # print all node
    def printbfs(self):
        pass

    # query nearest point
    def query(self, x):
        #scale = self.scale
        data = self.data
        stack = [self.root]
        #print 'query_start_root', len(self.root.rank)
        # print 'root scale and level', scale, self.root.level
        #res = []
        rank = -1
        D = 1000000000
        visit = {}
        # find all the node, which overlap with x
        while stack:
            node = stack.pop()
            #level = node.level
            y = data[node.key]
            if node.key not in visit:
                d = self.dist(x, y)
                visit[node.key] = d
            else:
                d = visit[node.key]
            if D > d:
                # print 'reduce D'
                rank, D = node.key, d
            #r = self.radius * pow(scale, level)
            r = node.radius
            if d <= 0:
                return [node.key]
            elif 0 < d <= r and len(node.child) > 1:
                stack.extend(node.child)
            else:
                continue

        # print 'search times', flag
        # print 'all leaves', len(self.leaf(self.root))
        # return [elem for elem in ranks if self.dist(x, data[elem]) <= err]
        return [rank]


    def query_rad(self, x, err=0):
        #scale = self.scale
        data = self.data
        stack = [self.root]
        #print 'root scale and level', scale, self.root.level
        #print 'query_start_root', len(self.root.rank)
        #res = []
        rank = -1
        D = 1000000000
        #D = float('inf')
        visit = {}
        nns = []
        # find all the node, which overlap with x
        while stack:
            node = stack.pop()
            #print 'query_node_rank', len(node.rank), 'root', len(self.root.rank)
            #level = node.level
            y = data[node.key]
            if node.key not in visit:
                d = self.dist(x, y)
                visit[node.key] = d
            else:
                d = visit[node.key]
            if D > d:
                # print 'reduce D'
                rank, D = node.key, d
            #r = self.radius * pow(scale, level)
            r = node.radius
            if d <= err - r:
                #print 'in the ball', len(node.rank)
                nns.extend(node.rank)
            elif err - r < d <= err + r:
                #print 'overlap the ball', len(node.rank), len(node.child)
                #if len(node.rank) < 1000 or len(node.rank) < 2 * len(node.child):
                if node.num < self.chk:
                    #for idx in node.rank:
                    leaves = self.leaf(node)
                    for idx in leaves:
                        if idx not in visit:
                            y = data[idx]
                            d = self.dist(x, y)
                            visit[idx] = d
                        else:
                            d = visit[idx]
                        if d <= err:
                            #print 'overlap the ball', len(node.rank), len(node.child)
                            nns.append(idx)
                else:
                    stack.extend(node.child)
            else:
                #print 'd', d, 'err', err, 'r', r, 'idx', node.key
                continue

            '''
            if d <= err:
                #return [node.key]
                #nns.append(node.key)
                for idx in node.rank:
                    if idx not in visit:
                        y = data[idx]
                        d = self.dist(x, y)
                        visit[idx] = d
                    else:
                        d = visit[idx]
                    if d <= err:
                        nns.append(idx)

            elif err < d <= r and len(node.child) > 1:
                stack.extend(node.child)
            else:
                continue
            '''

        return len(nns) > 0 and nns or [rank]

        # print 'search times', flag
        # print 'all leaves', len(self.leaf(self.root))
        # return [elem for elem in ranks if self.dist(x, data[elem]) <= err]
        #return [rank]



    # query nearest point
    def query_radius(self, x, err=1e-2):
        # print '0 leaf', self.root_leaf()
        #err = max(self.dist(x, x), err)
        # print 'bias', err
        #err -= self.eps
        scale = self.scale
        data = self.data
        stack = [self.root]
        #stack = llist_nd([self.root])
        # print 'root scale and level', scale, self.root.level
        #res = []
        ranks = []
        # find all the node, which overlap with x
        flag = 0
        visit = {}
        # while stack:
        flag_flt = 0
        while len(stack) > 0:

            flag += 1
            node = stack.pop()
            #node = stack.popleft().val
            #key = node.key
            #level = node.level
            y = data[node.key]

            if node.key not in visit:
                d = self.dist(x, y)
                visit[node.key] = d
            else:
                d = visit[node.key]


            #print 'current dist xy', d, euclidean(x, y)
            #r = self.radius * pow(scale, level)
            r = node.radius
            # print 'stack length', len(stack)
            # print 'stack visit'
            # print 'current find d', d, 'r', r, 'err', err, 'key', node.key,
            # 'child', len(node.child), d <= err + r, len(node.child) > 1, d <=
            # err +self.eps, node.rank, len(self.leaf(node))

            # if d + r <= err:
            if d + r <= err + self.eps:

                leaves = self.leaf(node)
                ranks.extend(leaves)
                # if x == self.data[len(self.data) // 2]:
                #    print 'radius is', r, 'd is', d, 'err', err, leaves, len(leaves), 'max number', Max([mannwhitneyu_c(x, self.data[elem]) for elem in leaves])
                # print 'radius is', r, 'd is', d, 'err', err, leaves,
                # len(leaves), 'max_mann', Max([mannwhitneyu_c(x,
                # self.data[elem]) for elem in leaves])
                #print 'found inner dist', d, err, r, 'x'
            elif node.num <= self.chk and d <= err + r + self.eps:
                leaves = self.leaf(node)
                #ranks.extend(leaves)
                for lf in leaves:
                    y = self.data[lf]
                    if lf in visit:
                        ds = visit[lf]
                    else:
                        ds = self.dist(x, y)
                        flag_flt += 1
                    if ds <= err:
                        ranks.append(lf)

            # elif d <= err + r and len(node.child) > 1:
            # elif d <= err + r:
            elif d <= err + r + self.eps:
                # print 'yes, overlap', 'key', node.key, 'err', err, 'd', d, 'r', r, [elem.key for elem in node.child], len(self.leaf(node))
                # if len(node.child) >= 1:
                # if len(node.child) > 0:
                #    stack.extend(node.child)
                stack.extend(node.child)
                # if node is leaf, then add to ranks list
                # else:
                #    #if d <= err + self.eps:
                #    if d <= err:
                #        if node.rank:
                #            ranks.extend(node.rank)
                #        else:
                #            ranks.append(node.key)
                #print 'found overlap', d, err, r, 'x'
            else:
                #print 'found outer dist', d, err, r, 'x'
                continue

        print 'search times', flag, flag_flt
        # print 'all leaves', len(self.leaf(self.root))
        # return [elem for elem in ranks if self.dist(x, data[elem]) <= err]
        # if x == self.data[len(self.data) // 3]:
        #    print 'idx rank is', len(ranks), len(self.data) // 3

        return ranks


# def run(x, y, n):
def run(n, qry):
    ksize = max(2, n)
    rg = rrandom.Random()
    a = []
    for i in xrange(n):
        #b = [r_ushort(int(rg.random() * pow(2, 15) - 1)) for elem0 in xrange(32)]
        b = [int(rg.random() * pow(2, 15) - 1) for elem0 in xrange(32)]
        # b.sort()
        TimSort(b).sort()
        # a.append(b)
        a.append([r_ushort(elem) for elem in b])
        # a.append(d)
    #a = [TimSort([r_ushort(int(rg.random() * pow(2, 15) - 1)) for elem0 in xrange(32)]).sort() for elem1 in xrange(n)]
    # print 'short add', a[0][0] + a[0][0]
    u = p = 0
    Atmp = range(6)
    dna = 'atgcgc'
    qsort(Atmp, dna)
    print 'qsort', Atmp, [dna[elem] for elem in Atmp]
    for i in xrange(1):
        x = [0] * 32
        y = [0] * 32
        # for j in xrange(32):
        #    x[j] = rg.random()
        #    y[j] = rg.random()
        #x = [rg.random() for elem in xrange(32)]
        #y = [rg.random() for elem in xrange(32)]
        #x = [intmask(elem) for elem in [r_ushort(0)] * 32]
        #x = map(intmask, [0] * 32)
        y = [intmask(elem) for elem in xrange(32)]
        #rgs = range(32)
        #y = map(intmask, rgs)
        #x = y = [0] * 32
        u, p = mannwhitneyu(x, y, True)
        p = pearson(x, y)

    print 'p value is', u, p

    print k2n('ta' * 12), intmask(int('123'))
    test_seq = 'tgatcgctgtagctgatgctcatgctatgctatcgtagtcgtgctagctagcatcgatcgatcgctagaaacagctgcgtatctatctatatatatattaggagaatgtgagaga'
    test_n = seq2n(test_seq)
    # for i in test_n:
    #    print 'seq2n test', i
    canopy(a)

    print [r_uint(elem) for elem in test_n]
    buck = [[r_ushort(0) for elem0 in xrange(pow(scale, ksize))]
            for elem1 in xrange(len(qry))]
    f0 = open(qry, 'r')
    f1 = open(qry, 'r')
    seqs0 = parse(f0)
    seqs1 = parse(f1)
    for seq0, seq1 in izip([seqs0, seqs1]):
        # print seq0.seq, seq1.seq
        print 'test seq2n'
        # print [nb for nb in seq2n(seq0.seq)]
        kmc(seq0.seq, buck[0], ksize, scale)
        kmc(seq1.seq, buck[0], ksize, scale)

    f0.close()
    f1.close()

    print [intmask(elem) for elem in buck[0][:15]]
    '''
    while 1:
        try:
            seq0 = seqs0.next()
            seq1 = seqs1.next()
            print seq0.seq, seq1.seq
        except:
            break

    return 1
    '''


# random sample from a list
def sample(x, n):
    N = len(x)
    if N < n:
        n = N
    y = [x[int(random() * N)] for elem in xrange(n)]
    qsort(y)
    return y


def entry_point0(argv):
    try:
        K = int(argv[1])
    except:
        K = 10
    try:
        qry = float(argv[2])
    except:
        qry = 10

    dna = 'agatgctagtcgtagctagctagcatcgatcgatcgatcgatcgatgcacga'
    dna = dna.upper()
    print rc(dna)
    print longest_orf(dna)
    print codon_bias(dna)
    t0 = time()
    for i in xrange(int(qry)):
        rc(dna)
        longest_orf(dna)
        codon_bias(dna)

    #tp = [[1, 2], [3, 2]]
    # qsort(tp)

    print 'qry', qry, 'time is', time() - t0

    #fac = lambda x: sum(range(x))
    # print fac(K)

    #x = range(32)
    #y = range(32, 64)
    #run(x, y, K)
    #run(K, qry)

    # test qsort
    #random = rrandom.Random().random
    #a = [random() for elem in xrange(int(qry))]
    #qsort(a, lambda x: -x)
    # print a[:10]

    t0 = time()
    d1 = []
    for i in xrange(K):
        #b = [int(random() * pow(2, 15) - 1) for elem0 in xrange(32)]
        #b = [int(((random() - .5) * 2 + i % 10) * 10) for elem0 in xrange(32)]
        b = [random() + i % 10 for elem0 in xrange(32)]
        # TimSort(b).sort()
        qsort(b)
        #d1.append([r_ushort(elem) for elem in b])
        d1.append(b)
        # d1.append(b)
    print 'after sorting', K, time() - t0, d1[0]
    d1[int(K) * 10]
    d1.extend(d1)

    # ks test
    print 'ks test', ks_test(d1[0], d1[0]), ks_test(d1[0], d1[1])

    idx = len(d1) // 2
    test = [mannwhitneyu_c(d1[idx], elem) for elem in d1]
    flag = -1
    for i in test:
        if flag < i:
            flag = i

    print 'naive pass test', len(
        [elem for elem in test if elem == 0]), len(test), flag

    Tree = Cvt(d1)
    t0 = time()
    Tree.fit()
    Tree.printbfs()
    print 'construct time', time() - t0

    #test = Tree.query(d1[0])
    test = [mannwhitneyu_c(d1[idx], d1[elem]) for elem in Tree.query(d1[idx])]
    flag = -1
    for i in test:
        if flag < i:
            flag = i
    # , Tree.query(d1[1])
    print 'cvt tree pass test', len(
        [elem for elem in test if elem == 0]), len(test), flag

    qry = int(qry)
    if qry < 0:
        qry = 0

    t0 = time()
    flag = 1
    # for y in d1[: qry]:
    for i in xrange(qry):
        # break
        y = d1[i]
        #Tree.query(d1[0]), mannwhitneyu_c(d1[0], d1[0])
        out = Tree.query_radius(y, 1e-3)

        if flag % 10000 == 0:
            error = 1000000000
            idx = -1
            for j in out:
                err = mannwhitneyu_c(y, d1[j])
                if err < error:
                    error = err
                # print 'error and err', error, err, err < error and err or
                # error

                idx = j
            # print 'query time', time() - t0, 'error', error, idx, out[:10],
            # len(out)
            print '10000 query time', time() - t0

            t0 = time()
        flag += 1

    #mannwhitneyu_c(x, y)

    #test = [mannwhitneyu_c(d1[0], y) for y in d1]
    # print 'real', [elem for elem in test if elem <= 1e-2]
    # print 'real', [[elem, mannwhitneyu_c(d1[0], d1[elem])] for elem in
    # xrange(len(d1)) if mannwhitneyu_c(d1[0], d1[elem]) <= 1e-2]

    # print 'debugging'
    error = 10. / len(d1) < 1e-6 and 10. / len(d1) or 1e-6
    #error = 0
    print 'debugging error', error
    idx = len(d1) // 3

    idx2 = Tree.query(d1[idx])[0]
    print 'query function', mannwhitneyu_c(d1[idx2], d1[idx]), idx2, idx

    tmp0 = [int(elem) for elem in xrange(len(d1))
            if mannwhitneyu_c(d1[idx], d1[elem]) <= error]
    tmp1 = [int(elem) for elem in Tree.query_radius(d1[idx], error)]
    qsort(tmp0)
    qsort(tmp1)
    print 'linear search pts', len(tmp0), Max(
        [mannwhitneyu_c(d1[idx], d1[int(etmp)]) for etmp in tmp0])
    t0 = time()
    print 'cover tree search', len(tmp1), sum([mannwhitneyu_c(
        d1[idx], d1[elem]) <= error for elem in Tree.query_radius(d1[idx], error)]), 'time', time() - t0
    # canopy(d1)
    print 'cover search length', len(Tree.query_radius(d1[idx], error)), idx

    # print centroid(d1)
    #d1 = [[intmask(1)] * 64 for elem in xrange(K)]
    print 'dbscan', len(d1)
    t0 = time()
    cluster = dbscan(d1)
    print 'cluster type is', time() - t0
    # print 'cluster size', len(cluster), len(cluster[0]), len(noise)
    #label = dbscan(d1)
    #flag = 0
    # for i in label:
    #    flag = flag < i and i or flag
    # print flag
    #aset = {}
    #aset[0] = 1
    # print kmean(d1)

    #d2 = [r_ushort(1)] * K
    #d3 = []
    # while d2:
    #    d3.append(d2.pop())

    # print 'print before extend d3', len(d3)
    # d3.extend(d3[:5])
    # print 'print after d3', len(d3)
    # d2.append(['abc'])
    # print 'pop last', intmask(d3.pop())
    #d2 = [[r_ushort(1)] * K, [r_ushort(4), r_ushort(4)] * K]
    # print 'D2 shape', len(d2), len(d2[1])
    #del d2;
    #a = [1, 2, 3 ,4]
    # heappop(a)
    gc.collect()
    #buck = fq2c(argv[1:])

    return 0


def entry_point(argv):
    qry = argv[1]

    try:
        prs = float(argv[2])
    except:
        prs = .2

    try:
        start = int(argv[3])
    except:
        start = 0

    try:
        end = int(argv[4])
    except:
        end = 2**61

    try:
        sparse = argv[5]
    except:
        sparse = 'n'

    #dist_func = pdist_sp
    #get_x = get_row_sp
    #Pearson = pearson_sp

    #dist_func = pdist
    dist_func = euclidean
    get_x = get_row
    Pearson = pearson

    data = []
    flag = -1
    n2s = []
    dim = -1

    f = open(qry, 'r') 
    for i in readline(f):
        if flag < start:
            dim = len(i[:-1].split(',')) - 16
            flag += 1
            continue

        if flag >= end:
            break

        flag += 1
        J = i[:-1].split(',')

        n2s.append(J[0])
        dat3 = get_x(i,start=16)
        if len(dat3) != dim and dim != -1:
            continue

        dat3 = normalize(dat3)
        data.append(dat3)

    print 'final iter', flag
    f.close()

    cut = p2d(prs, 1)
    print 'cut dist', cut, dim
    # build small tree
    Tree = RPT(data[:3], norm=lambda x:x)
    #hpl = Tree.hyperplane(data[0])
    hpl = normalize([random() for elem in xrange(dim)])

    Nd = len(data)
    for i in xrange(Nd):
        #if i > end:
        if 1:
            break
        for j in xrange(Nd):
            x, y = data[i], data[j]
            print i, j, 'pdist', pdist(x, y, 1), euclidean(x, y),'dist2hyper', Tree.p2h(x, hpl), Tree.p2h(y, hpl)


    #Tree = RPT(data, norm=lambda x: x)
    Tree = VP(data, norm=lambda x: x)
    Tree.fit()
    flag = 0
    for i in data:
        print 'searching', n2s[flag], prs
        js = Tree.query(i, cut)
        #print 'js length', len(js)
        for jd in js:
            j, d = jd[:2]
            j = int(j)
            y = data[j]
            pr = d2p(d, 1)
            #pr = pearson(i, y)
            if pr >= prs:
                #print n2s[flag], n2s[j], pearson(i, y)
                print n2s[flag], n2s[j], pr

            #print n2s[flag], n2s[j]

        flag += 1

    return 0




    Tree = Cvt(data, dist=dist_func)
    Tree.fit()
    #cut = p2d(prs, dim)
    cut = p2d(prs, 1)
    flag = -1
    print 'current cut', cut
    f = open(qry, 'r') 
    for i in readline(f):
        if flag == -1:
            flag = 0
            continue

        J = i[:-1].split(',')
        dat3 = get_x(i, start=16)
        dat3 = normalize(dat3)
        mx = 0.
        mi = 1
        target = Tree.query_radius(dat3, cut)
        #target = Tree.query_rad(dat3, cut)

        for t in target:
            tmp = Pearson(dat3, data[t])
            mi = tmp < mi and tmp or mi
            if tmp < prs:
                mx += 1.
            print J[0], n2s[t], tmp
        print 'error', mx / len(target), len(target), 'iter', flag, cut, 'min', mi
        flag += 1

    f.close()

    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    import sys
    entry_point(sys.argv)
