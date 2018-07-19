#!usr/bin/env python
import numpy as np
import sys
from scipy.stats import pearsonr


def get_row(x, start=0, sep=','):
    j = x[:-1].split(sep)
    h = j[0]
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
    return h, zs


def normal(X):
    x = X - X.mean()
    y = np.dot(x, x) ** .5
    return (x + 1e-9) / (y + 1e-9)


def main():
    qry = sys.argv[1]
    try:
        thres = eval(sys.argv[2])
    except:
        thres = .2

    f = open(qry, 'r')
    n2s = {}
    data = []
    #data_row = []
    flag = 0
    for i in f:
        h, j = get_row(i, 16)
        j = np.asarray(j, 'float32')
        #data_row.append(j)
        j = normal(j)
        j = np.nan_to_num(j)
        data.append(j)
        n2s[flag] = h
        flag += 1
        #if flag > 10000:
        #    break

    data = np.asarray(data)
    f.close()

    N, D = data.shape
    #p = hnswlib.Index(space='ip', dim=D)
    #p.init_index(max_elements=N, ef_construction=100, M=16)
    # p.set_ef(10)
    # p.add_items(data)

    chk = 10000
    for i in xrange(0, N, chk):
        # caculate pearson cor
        prs = np.dot(data, data[i:i + chk].T)
        rows, cols = np.where(prs >= thres)
        cols += i
        for j in xrange(rows.size):
            r, c = rows[j], cols[j]
            rs, cs = map(n2s.get, [r, c])
            print rs, cs, prs[r, c]
            #print rs, cs, prs[r, c], pearsonr(data_row[r], data_row[c])[0]



if __name__ == '__main__':
    main()
