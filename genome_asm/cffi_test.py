#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-11 17:33:21

#from array import array
import numpy as np
from cffi import FFI
import sys

clf = FFI()
try:
    N = int(eval(sys.argv[1]))
except:
    N = 1000

#a = np.empty((N, N), dtype = 'int32')
a = np.memmap('test.npy', mode = 'w+', shape = (N, N), dtype = 'int32')

b = clf.cast('int [%d][%d]'%(N, N), clf.from_buffer(a))

for i in xrange(N):
    for j in xrange(N):
        b[i][j] = 2 ** 31 - 1

for i in xrange(N):
    for j in xrange(N):
        if b[i][j] != 2 ** 31 -1:
            print 'found'

print b[i][j], N * N / 1e8
