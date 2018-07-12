#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-30 19:55:05

from sklearn import cluster
import numpy as np
import sys

N = int(eval(sys.argv[1]))

a = np.random.randn(N, 32)

clf = cluster.DBSCAN(algorithm = 'auto', eps = 1)
clf.fit(a)
print clf.labels_.max()
