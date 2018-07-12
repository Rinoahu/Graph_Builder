#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2017-01-19 09:44:51

import numpy as np
import math
from math import erfc
import sys
from random import random
from collections import Counter
from itertools import izip

UNCLASSIFIED = False
NOISE = None


# Cumulative Normal Distrubtion
ncdf = lambda x : erfc(-x / 1.4142135623730951) / 2

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
                #print 'hello', ri, i, start
                for j in xrange(start, i):
                    rank[j] = ri

            start = i
        else:
            end = i

    if start < end:
        ri = float(start + end) / 2.
        ts.append(n - start)
        #print 'hello', ri
        for j in xrange(start, n):
            rank[j] = ri

    # correct start from 0
    #for i in xrange(n):
    #    rank[i] += 1

    return rank, ts



# tiecorrect
tiecorrect = lambda ts, n: ts and 1 - sum([t ** 3. - t for t in ts]) / (n ** 3 - n) or 1

# Mann–Whitney U test
# return the z score of U
def mannwhitneyu(x, y, use_continuity = True, alternative = 'two-sided'):
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
    #print 'z u0 u1 u mu sigma n0 n1 n'
    if z >= 0:
        p = 2 - 2 * ncdf(z)
    else:
        p = 2 * ncdf(z)
    #return u, p
    #return abs(z)
    return p


def _dist(p,q):
	return math.sqrt(np.power(p-q,2).sum())

def _eps_neighborhood(p,q,eps):
	#return _dist(p,q) < eps
        return mannwhitneyu(sorted(p), sorted(q)) >= eps

def _region_query(m, point_id, eps):
    n_points = len(m[0])
    seeds = []
    for i in xrange(0, n_points):
        x = [m[elem][point_id] for elem in xrange(len(m)) ]
        y = [m[elem][i] for elem in xrange(len(m)) ]
        #if _eps_neighborhood(m[:,point_id], m[:,i], eps):
        if _eps_neighborhood(x, y, eps):

            seeds.append(i)
    return seeds

def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    seeds = _region_query(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id
        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                       classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True
        
def dbscan(m, eps, min_points):
    """Implementation of Density Based Spatial Clustering of Applications with Noise
    See https://en.wikipedia.org/wiki/DBSCAN
    
    scikit-learn probably has a better implementation
    
    Uses Euclidean Distance as the measure
    
    Inputs:
    m - A matrix whose columns are feature vectors
    eps - Maximum distance two points can be to be regionally related
    min_points - The minimum number of points to make a cluster
    
    Outputs:
    An array with either a cluster id number or dbscan.NOISE (None) for each
    column vector in m.
    """
    row, col = len(m), len(m[0])
    cluster_id = 1
    n_points = len(m[1])
    classifications = [UNCLASSIFIED] * n_points
    for point_id in xrange(0, n_points):
        #point = m[:,point_id]
        point = [m[elem][point_id] for elem in xrange(len(m))]

        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    return classifications

def test_dbscan(N):
    #m = np.matrix('1 1.2 0.8 3.7 3.9 3.6 10; 1.1 0.8 1 4 3.9 4.1 10')
    m = [[random() + elem % 10 for elem in xrange(N)] for j in xrange(32)]
    eps = 0.8
    min_points = 5
    #assert dbscan(m, eps, min_points) == [1, 1, 1, 2, 2, 2, None]
    output = Counter(dbscan(m, eps, min_points))
    print output, len(output)



N = int(eval(sys.argv[1]))
test_dbscan(N)
