#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-05 15:44:22
#from collections import Counter
from Bio import SeqIO
from array import array
#import numpy as np
from math import sqrt, erf, erfc
from random import shuffle
from time import time
from itertools import izip
from multiprocessing import Pool
import multiprocessing as mp
from functools import partial


# the sequence class
class Seq:

    def __init__(self, id=None, seq=None, description=None, qual=None):
        self.id = id
        self.seq = seq
        self.description = description
        self.qual = qual

    def update(self, id=None, seq=None, description=None, qual=None):
        self.id = id
        self.seq = seq
        self.description = description
        self.qual = qual

# parse the fastq or fasta


def parse(f, mode='fastq'):
    seq = Seq()
    output = []
    for i in f:
        if len(output) == 4:
            #seq.id, seq.seq, seq.description, seq.qual = output
            seq.update(*output)
            yield seq
            output = [i[: -1]]
        else:
            output.append(i[: -1])

    if len(output) == 4:
        #seq.id, seq.seq, seq.description, seq.qual = output
        seq.update(*output)
        yield seq

# calculate codon's relative frequency from orf of gene


def codonfreq(orf):
    # for i in orf[::3]
    n = len(orf)
    freq = {}
    for i in xrange(0, n, 3):
        pass


mean = lambda x: 1. * sum(x) / len(x)


def std(x):
    if len(x) <= 1:
        return 0
    else:
        m = mean(x)
        var = sum([(elem - m) * (elem - m) for elem in x]) / (len(x) - 1.)
        return var ** .5


# the euclidean distance
def euclidean(x, y):
    d = 0
    for i in xrange(len(x)):
        z = (x[i] - y[i])
        d += z * z

    return sqrt(d)

# dist between x and y
# the dist can be normalized by the norm of x or y


def dist(x, y, n=0):
    nx, ny, nz = [elem ** .5 for elem in map(sum, [[xi ** 2 for xi in x], [
                                             yi ** 2 for yi in y], [(yi - xi) ** 2 for xi, yi in zip(x, y)]])]
    return n == 0 and nz / nx or nz / ny


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


# Cumulative Normal Distrubtion
ncdf = lambda x: erfc(-x / 1.4142135623730951) / 2

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
tiecorrect = lambda ts, n: ts and 1 - \
    sum([t ** 3. - t for t in ts]) / (n ** 3 - n) or 1

# Mann–Whitney U test
# return the z score of U


def mannwhitneyu(x, y, use_continuity=True, alternative='two-sided'):
    n0, n1 = map(len, [x, y])
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
    rank0 = sum([a for a, b in izip(rank, lab) if b == 0]) + n0

    u0 = n0 * n1 + n0 * (n0 + 1) / 2. - rank0
    #u1 = n1 + sum([a for a, b in zip(rank, lab) if b == 1]) - n1 * (n1 + 1) / 2
    u1 = n0 * n1 - u0

    u = min(u0, u1)
    mu = n0 * n1 / 2.
    var = n0 * n1 * (n + 1) * tiecorrect(ts, n) / 12.
    sd = var ** .5
    z = use_continuity and abs(u - mu) - .5 / sd or abs(u - mu) / sd
    # print 'z u0 u1 u mu sigma n0 n1 n'
    if z >= 0:
        p = 2 - 2 * ncdf(z)
    else:
        p = 2 * ncdf(z)
    # return u, p
    # return abs(z)
    return p

# ks test


def ks_test(x, y):
    pass


# compare whether two dataset belong to same distrubtion, use the correlation
def curve_cor(s0, s1, bins=20):
    up = max(map(max, s0, s1))
    lo = min(map(min, s0, s1))
    inc = (up - lo + 1.) / bins
    h0, h1 = [0] * bins, [0] * bins
    for i in s0:
        j = int((i - lo) // inc)
        h0[j] += 1.

    for i in s1:
        j = int((i - lo) // inc)
        h1[j] += 1.

    return pearson(h0, h1)

# draw the kmer-freq distrubtion from sequence
# remove the extreme point


def khist(s, bins=20):

    # remove extreme point
    u, r = mean(s), std(s)
    # lower and up bound
    lb, ub = u - r, u + r
    S = [elem for elem in s if lb <= elem <= ub]
    # print 'remove', len(s) - len(S), u, r, lb, ub
    if not S:
        S = s

    # get kmer hist
    up, lo = max(S), min(S)
    inc = (up - lo + 1.) / bins
    h = [0] * bins
    for i in S:
        j = int((i - lo) // inc)
        h[j] += 1

    return h, lo, up, inc

# 2d matrix class which is memory-efficent


class mat:

    def __init__(self, data=None, shape=None, dtype='f'):
        if dtype == 'int32':
            self.dtype = 'i'
        elif dtype == 'uint32':
            self.dtype = 'I'
        elif dtype == 'int16':
            self.dtype = 'h'
        elif dtype == 'uint16':
            self.dtype = 'H'
        elif dtype == 'b':
            self.dtype = 'h'
        elif dtype == 'B':
            self.dtype = 'H'
        elif dtype == 'float':
            self.dtype = 'f'
        else:
            self.dtype = 'd'
        assert len(shape) == 2
        self.shape = shape
        self.data = data
        #self.data = array(self.dtype)
        # self.data.extend(data)
        self.NONE = slice(None, None, None)

    # get elem
    def __getitem__(self, (x, y)):
        NONE = self.NONE
        # print 'x', x, x is NONE
        # print 'y', y, y is NONE
        X, Y = self.shape
        if isinstance(x, int):
            assert x < X
        if isinstance(y, int):
            assert y < Y

        # if x != NONE and y != NONE:
        if not isinstance(x, slice) and not isinstance(y, slice):
            out = self.data[Y * x + y]
        # elif x != NONE and y == NONE:
        elif not isinstance(x, slice) and isinstance(y, slice):
            start = Y * x
            out = self.data[start: start + Y]
        # elif x == NONE and y != NONE:
        elif isinstance(x, slice) and not isinstance(y, slice):
            out = array(self.dtype)
            for i in xrange(X):
                out.append(self.data[Y * i + y])
        else:
            out = self.data

        return out

    # set elem
    def __setitem__(self, (x, y), z):
        X, Y = self.shape
        if isinstance(x, int):
            assert x < X
        if isinstance(y, int):
            assert y < Y

        # if x != NONE and y != NONE:
        if not isinstance(x, slice) and not isinstance(y, slice):
            self.data[Y * x + y] = z
        # elif x != NONE and y == NONE:
        elif not isinstance(x, slice) and isinstance(y, slice):
            start = Y * x
            self.data[start: start + Y] = z
        # elif x == NONE and y != NONE:
        elif isinstance(x, slice) and not isinstance(y, slice):
            for i in xrange(X):
                self.data[Y * i + y] = z
        else:
            self.data[:] = z

    def __iter__(self):
        for i in xrange(self.shape[0]):
            yield self[i, :]

    def __len__(self):
        return self.shape[0]

# dist calculation for one vs many


def Mdist(rg, q, data, dist=mannwhitneyu):
    start, end = rg
    x, shape = data
    xs = mat(x, shape)
    return [dist(q, xs[elem, :]) for elem in xrange(start, end)]


def mdist(z):
    rg, q, dist = z
    start, end = rg
    x, shape = data
    xs = mat(x, shape)
    return [dist(q, xs[elem, :]) for elem in xrange(start, end)]


# parallel for Mdist
def Pmdist(q, t, dist=mannwhitneyu):
    shape = t.shape
    raw = t.data
    data = (raw, shape)
    global data
    #dist = partial(Mdist, q = q, data = (raw, shape), dist = dist)
    step = 10000
    rg = range(0, shape[0], step) + [shape[0]]

    pool = Pool()
    output = pool.map(mdist, [[(i, j), t[0, :], dist]
                              for i, j in zip(rg[::-1], rg[1::])])
    return output
    # return pool.map(dist, [(i, j) for i, j in zip(rg[::-1], rg[1::])])


# the canopy algoithm
# for euc, t1 > t2
# for cor, t1 < t2
# def canopy(data, t1 = 2., t2 = 1.5, dist = pearson):
def canopy(data, t1=0, t2=1e-3, dist=mannwhitneyu):
    #canopies = []
    canopies = open('canopies.npy', 'w')
    #idxs = range(len(data))
    idxs = array('i')
    for i in xrange(len(data)):
        idxs.append(i)

    # shuffle the index
    shuffle(idxs)

    # the can and keep array
    #can = array('i')
    #keep = array('i')

    flag = 0
    while idxs:
        idx = idxs.pop()
        x = data[idx, :]

        #can = [idx]
        can = array('i', [idx])
        #del can[:]
        # can.append(idx)

        #keep = []
        keep = array('i')
        #del keep[:]

        if dist == pearson or mannwhitneyu:
            print 'pearson'
            for elem in idxs:
                # while idxs:
                #    elem = idxs.pop()
                if dist(x, data[elem, :]) > t1:
                    can.append(elem)
                if dist(x, data[elem, :]) < t2:
                    keep.append(elem)
                # print 'size', len(idxs)
        else:
            for elem in idxs:
                # while idxs:
                #    elem = idxs.pop()
                if dist(x, data[elem, :]) < t1:
                    can.append(elem)
                if dist(x, data[elem, :]) > t2:
                    keep.append(elem)

        # canopies.append(can)
        # use -1 as sep and save to disk
        can.append(-1)
        can.tofile(canopies)
        print 'can size', len(can), len(keep)
        del can, idxs
        idxs = keep

    canopies.close()
    return canopies


# the ATGC code
code = [0] * 256
flag = 0
for i in 'ATGC':
    code[ord(i.lower())] = code[ord(i)] = flag
    flag += 1

scale = max(code) + 1


# fast convert kmer to number
def k2n(s, scale=4, code=code):
    if scale == -1:
        scale = code.max() + 1
    N = 0
    output = 0
    for i in s[::-1]:
        output += code[ord(i)] * scale ** N
        #output += code[ord(i)] * pow(scale, N)
        N += 1

    return output

# use the current s2n value to calcuate the next one
#s2n_next = lambda start, ksize, scale, code, char: start % (scale ** (ksize - 1)) * scale + code[ord(char)]
s2n_next = lambda start, ksize, scale, code, char: start % (
    pow(scale, (ksize - 1))) * scale + code[ord(char)]


# convert kmer to number from a seq
def seq2n(s, k=15, scale=4, code=code):
    if len(s) <= k:
        yield k2n(s, scale, code)
    else:
        start = k2n(s[: k], scale, code)
        yield start
        for i in s[k:]:
            start = s2n_next(start, k, scale, code, i)
            yield start


# generate the kmer frequence table
def kmc(seq, buck, k=5, scale=4, code=code):
    N = len(seq)
    for i in xrange(N - k + 1):
        start = k2n(seq[i: i + k], scale=scale, code=code)
        buck[start] += 1

# fast version of generate the kmer frequence table


def fkmc(seq, buck, k=5, scale=4, code=code):
    for i in seq2n(seq, k, scale, code):
        val = buck[i]
        if val < 65535:
            buck[i] = val + 1


# whether a col is all zero
col_zero = lambda buck, i, N: not any([buck[elem][i] for elem in xrange(N)])

# compress the array by del all zeros col


def compress(buck):
    p0 = p1 = 0
    N, D = map(len, [buck, buck[0]])
    print 'before', D
    while 1:
        while not col_zero(buck, p0, N) and p0 < D:
            # print 'all zero'
            p0 += 1

        while p1 < N and (col_zero(buck, p1, N) or p1 <= p0):
            # print 'not all zero'
            p1 += 1

        if p0 < p1 < D:
            # print 'change'
            for i in xrange(N):
                buck[i][p0], buck[i][p1] = buck[i][p1], buck[i][p0]
        else:
            break

    for i in xrange(N - 1, -1, -1):
        if col_zero(buck, i, N):
            for j in xrange(N):
                buck[j].pop()
        else:
            break

    print 'after', len(buck[0])


# count the kmer from the paired fastq file
def fq2c(qry):
    k = int(eval(qry[0]))
    names = qry[1:]
    D = len(names)
    scale = 4
    buck = [array('H', [0]) * pow(scale, k) for elem in xrange(D // 2)]
    #buck = [array('H', [0]) * scale ** k for elem in xrange(D // 2)]
    #buck = np.zeros((D//2, scale ** k), 'int32')
    flag = 0
    itr = 1
    init0 = init1 = time()
    for qry0, qry1 in zip(names[::2], names[1::2]):
        print 'qry0', qry0, 'qry1', qry1
        f0 = open(qry0, 'r')
        f1 = open(qry1, 'r')
        seqs0 = parse(f0, 'fastq')
        #seqs0 = SeqIO.parse(f0, 'fastq')
        seqs1 = parse(f1, 'fastq')
        #seqs1 = SeqIO.parse(f1, 'fastq')
        for i0, i1 in izip(seqs0, seqs1):
            if i0.qual.count('N') > 20 or i1.qual.count('N') > 20:
                continue

            fkmc(i0.seq, buck[flag], k, scale)
            fkmc(i1.seq, buck[flag], k, scale)

            # timing
            if itr % 1000000 == 0:
                print 'iteration', itr, 'time', time() - init1, 'total time', time() - init0
                init1 = time()
            itr += 1

        f0.close()
        f1.close()

        flag += 1

    # convert the each reads to a freq hist
    flag = 0
    itr = 1
    init0 = init1 = time()
    for qry0, qry1 in zip(names[::2], names[1::2]):
        print 'qry0', qry0, 'qry1', qry1
        f0 = open(qry0, 'r')
        f1 = open(qry1, 'r')
        seqs0 = parse(f0, 'fastq')
        #seqs0 = SeqIO.parse(f0, 'fastq')
        seqs1 = parse(f1, 'fastq')
        #seqs1 = SeqIO.parse(f1, 'fastq')
        for i0, i1 in izip(seqs0, seqs1):
            if i0.qual.count('N') > 20 or i1.qual.count('N') > 20:
                continue

            output = []
            fwd = [buck[flag][elem] for elem in seq2n(i0.seq, k, scale, code)]
            rev = [buck[flag][elem] for elem in seq2n(i1.seq, k, scale, code)]
            med = len(fwd) // 2
            start, end = med - 16, med + 16
            # for test, only keep positive
            #output = fwd[start: end] + rev[start: end]
            output = fwd[start: end]
            output.sort()
            if len(output) < 32:
                output.extend([0] * (32 - len(output)))

            # print max(output), min(output), mean(output), std(output), output
            #A, B, C, D = khist(output)
            # print ' '.join(map(str, A + ['|', B, C, D]))
            # print ' '.join(map(str, output))

            # timing
            if itr % 1000000 == 0:
                print 'iteration', itr, 'time', time() - init1, 'total time', time() - init0
                init1 = time()
            itr += 1

        f0.close()
        f1.close()

        flag += 1

    return buck


if __name__ == '__main__':
    import sys
    from random import choice
    import random

    '''
    # test code
    N = 1 * 10 ** 7
    a = array('I')
    for i in xrange(N):
        b = [random.random() + (i / (N / 10)) for elem in xrange(32)]
        b.sort()
        #c = sum(b) / 100
        #d = [int(elem / c) for elem in b]
        d = [int(elem * 100) for elem in b]
        a.extend(d)

    x = mat(a, (N, 32), 'int8')
    y = canopy(x, dist = lambda x, y: abs(mannwhitneyu(x, y)))
    raise SystemExit()
    '''

    #
    if len(sys.argv[1:]) < 2:
        print 'python this.py k foo0_f.fq foo0_r.fq foo1_f.fq foo1_r.fq ... fooN_f.fq fooN_r.fq'
    buck = fq2c(sys.argv[1:])
    print sum(map(sum, buck)), len(buck), len(buck[0])
