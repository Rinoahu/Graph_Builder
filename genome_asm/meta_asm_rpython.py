#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-13 15:34:46

# from array import array
from math import sqrt, erf, exp, pow, log
import math
import itertools
# from itertools import izip
from random import random
from rpython.rlib import rrandom
from rpython.rlib.rfloat import erfc
from rpython.rtyper.lltypesystem.rffi import r_ushort, r_int
from rpython.rlib.rarithmetic import intmask, r_uint32, r_uint, string_to_int
from rpython.rlib import rfile
from rpython.rlib import rmmap
from rpython.rlib.listsort import TimSort
from rpython.rlib import listsort
#from struct import pack
from time import time, sleep
import gc
from heapq import heappush, heappop, heapreplace, heapify


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
class vertex:

    def __init__(self, val):
        self.val = val
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


def pack(dtype, val):
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

s2n_next = lambda start, ksize, scale, code, char: start % int(
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

    print 'ksize, names, D, N, buck shape', ksize, names, D, N, len(buck), len(buck[0])

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
ncdf = lambda x: erfc(-x / 1.4142135623730951) / 2


# the sum, mean and std of an array/list
def sum(x):
    flag = 0
    #a = [[1] * 100 for elem in xrange(pow(10, 6))]
    for i in x:
        flag += i
        # a.append(i)
    return flag

mean = lambda x: 1. * sum(x) / len(x)


def std(x):
    if len(x) <= 1:
        return 0
    else:
        m = mean(x)
        var = sum([(elem - m) * (elem - m) for elem in x]) / (len(x) - 1.)
        return sqrt(var)


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


ks_test_c = lambda x, y: 1 - ks_test(x, y)

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
tiecorrect = lambda ts, n: ts and 1 - \
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
mannwhitneyu_c = lambda x, y: 1 - mannwhitneyu(x, y)[1]


# the euclidean distance
def euclidean(x, y):
    d = 0
    for i in xrange(len(x)):
        z = (x[i] - y[i])
        d += z * z

    return sqrt(d)

# dist between x and y
# the dist can be normalized by the norm of x or y


def dist(x, y, norm=True):
    nx, ny, nz = [sqrt(elem) for elem in map(sum, [[xi * xi for xi in x],
                                                   [yi * yi for yi in y], [(yi - xi) * (yi - xi) for xi, yi in zip(x, y)]])]
    return norm and nz / nx or nz / ny

# the pearson relationship


def pearson(x, y):
    N, M = len(x), len(y)
    assert N == M
    x_m, y_m = mean(x), mean(y)
    a = b = c = 0.
    for i in xrange(N):
        xi, yi = x[i] - x_m, y[i] - y_m
        a += xi * yi
        b += xi * xi
        c += yi * yi

    d = sqrt(b * c)
    if d > 0:
        return a / d
    else:
        return b == c and 1. or 0.


# update centroid
acentroid = lambda cx, x, cy, y: [
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


# multiple child node
class Node:
    # def __init__(self, key, rank, level = 0, radius = 1):

    def __init__(self, key, rank, radius=1):
        self.key = key
        self.rank = rank
        #self.level = level
        self.radius = radius
        self.child = []

# cover tree


class Cvt:

    def __init__(self, data, eps=1e-8, dist=ks_test_c):

        self.data = data
        self.eps = eps
        self.scale = .2
        self.dist = dist
        radius = -1
        n = len(data)
        #flag = 0
        x = 0
        for y in xrange(1, n):
            current = self.dist(data[x], data[y])
            #radius = radius < current and current or radius
            radius = current if radius < current else radius
            #flag += current < self.scale and 1 or 0

        print 'current radius is', radius
        self.root = Node(0, range(n), radius)

        # print 'at least half', flag, self.scale
        #self.radius = radius
        #self.maxlevel = radius > 0 and int(log(radius, 2) + 1) or 1
        #self.maxlevel = log(12, 2)

    def fit(self):

        nodes = [self.root]
        #scale = self.scale
        while nodes:
            n0 = nodes.pop()
            #level = n0.level + 1
            #radius = self.radius * pow(scale, level)
            #cutoff = n0.radius * pow(scale, level)

            # if cutoff > self.eps and len(n0.rank) > 1:
            if n0.radius > self.eps and len(n0.rank) > 1:
                cutoff = n0.radius * self.scale
                # if n0.key == 0:
                #    print 'first node', radius, len(n0.rank)

                #flag = 0
                # print 'first x data', n0.key
                for (radius, rank) in self.split(n0.rank, cutoff):
                    # print 'split set size', len(rank), 'level', level, 'radius', radius, 'self radius', self.radius
                    #n1 = Node(rank[0], rank, level, radius)
                    # if radius < 0:
                    #    continue
                    n1 = Node(rank[0], rank, radius)
                    n0.child.append(n1)
                    nodes.append(n1)
                    #flag += 1
            elif n0.radius > self.eps and len(n0.rank) <= 1:
                print 'debug test'
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
    def split(self, rank, cutoff):
        rank[0], rank[-1] = rank[-1], rank[0]
        data = self.data
        while rank:
            #radius = -1
            radius = 0
            x = rank.pop()
            inner, outer = [x], []
            while rank:
                y = rank.pop()
                current = self.dist(data[x], data[y])
                if current <= cutoff:
                    #radius = radius < current and current or radius
                    radius = current if radius < current else radius
                    # if radius == -1:
                    # print 'radius', radius, 'current longest', current,
                    # 'change', radius < current

                    inner.append(y)
                else:
                    outer.append(y)

                # print 'current radius is', radius, current

            # print 'inner set size', len(inner)
            # if radius == -1:
            # print 'error radius', cutoff, [mannwhitneyu_c(data[inner[0]],
            # data[elem]) for elem in inner]
            yield radius, inner
            rank = outer

    # dfs get all leaves's data by give an inner node
    def leaf(self, n):
        nodes = [n]
        ranks = []
        while nodes:
            node = nodes.pop()
            if node.child:
                nodes.extend(node.child)
            else:
                ranks.extend(node.rank)

        return ranks

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

            else:
                continue

        # print 'search times', flag
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


def entry_point(argv):
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
    #qsort(tp)

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

    print 'naive pass test', len([elem for elem in test if elem == 0]), len(test), flag

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
    print 'cvt tree pass test', len([elem for elem in test if elem == 0]), len(test), flag

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
    print 'linear search pts', len(tmp0), Max([mannwhitneyu_c(d1[idx], d1[int(etmp)]) for etmp in tmp0])
    t0 = time()
    print 'cover tree search', len(tmp1), sum([mannwhitneyu_c(d1[idx], d1[elem]) <= error for elem in Tree.query_radius(d1[idx], error)]), 'time', time() - t0
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


def target(*args):
    return entry_point, None

if __name__ == "__main__":
    import sys
    entry_point(sys.argv)
