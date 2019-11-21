#!usr/bin/env python

# brute force method to calculate similarity matrix
import numpy as np
import sys
from scipy.stats import pearsonr
try:
    xrange = xrange
except:
    xrange = range


def get_row(x, start=0, sep='\t'):
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
    try:
        z = x / y
    except:
        z = (x + 1e-9) / (y + 1e-9)

    return z

# log2
def log2normal(x):
    z = np.log2(x+1e-3)
    return z


# print the manual
def manual_print():
    print 'Usage:'
    print '    python %s -i ' % sys.argv[0]
    print 'Parameters:'
    print '  -i: str. The name of a tab-delimited file. The 1st column stand for gene names/identifier and the rest columns stand for gene expression levels in different samples.'
    print '  -t: float. A threshold value to filter low-correlation genes. If the pearson correlation coefficient between gene i and j is less than the threshold, then, it will be set to 0. Default value is 0.2'
    print '  -o: str. The name of output file. The output is a 3 column tab-delimited file, The 1st and 2nd columns are gene names and the 3rd column is the weight.'
    print '  -m: int. Memory usage limitation. Deaault is 4GB'
    print '  -s: str. Character used to separate fields. Deaault is \\t'









def main():
    #qry = sys.argv[1]
    #try:
    #    thres = eval(sys.argv[2])
    #except:
    #    thres = .2

    argv = sys.argv
    # recommand parameter:
    args = {'-i': '', '-t': '.2', '-m': '4', '-s': '\t', '-o': 'output'}

    N = len(argv)
    for i in xrange(1, N):
        k = argv[i]
        if k in args:
            try:
                v = argv[i + 1]
            except:
                break
            args[k] = v

        elif k[:2] in args and len(k) > 2:
            args[k[:2]] = k[2:]

        else:
            continue

    if args['-i'] == '':
        manual_print()
        raise SystemExit()

    try:
        qry, thr, mem, sep, ref = args['-i'], float(eval(args['-t'])), float(eval(args['-m'])), args['-s'], args['-o']
    except:
        manual_print()
        raise SystemExit()


    _o = open(qry+'.npy', 'wb')
    f = open(qry, 'r')
    f.next()
    n2s = {}
    #data = []
    #data_row = []
    R = 0
    buf = []
    for i in f:
        if i.startswith('#'):
            continue
        h, j = get_row(i, 1, sep=sep)
        j = np.asarray(j, 'float32')
        #data_row.append(j)
        j = log2normal(j)
        j = np.nan_to_num(j)
        #data.append(j)
        C = j.size
        buf.append(j)
        n2s[R] = h
        R += 1
        #if flag > 10000:
        #    break
        #if R > 10000:
        #    break

        ram = len(buf) * C * 4
        #if len(buf) > 1000:
        if ram > mem * 2**29:
            buf = np.asarray(buf, 'float32')
            _o.write(buf.data[:])
            buf = []

    if buf:
        buf = np.asarray(buf, 'float32')
        _o.write(buf.data[:])
        buf = []


    #data = np.asarray(data)
    f.close()
    _o.close()

    data = np.memmap(qry+'.npy', mode='r', shape=(R, C), dtype='float32')
    data = np.asarray(data, 'float32')

    N, D = data.shape
    #p = hnswlib.Index(space='ip', dim=D)
    #p.init_index(max_elements=N, ef_construction=100, M=16)
    # p.set_ef(10)
    # p.add_items(data)

    #chk = 10000

    _o = open(ref, 'w')
    chk = mem * 2**27 // (D+N)
    chk = int(max(chk, 1))
    for i in xrange(0, N, chk):
        # caculate pearson cor
        prs = np.dot(data, data[i:i + chk].T).T
        rows, cols = np.where(np.abs(prs) >= thr)
        #cols += i
        outs = []
        for j in xrange(rows.size):
            r, c = rows[j], cols[j]
            rs, cs = map(n2s.get, [r, c+i])
            output = [rs, cs, prs[r, c]]
            tmp = '\t'.join(map(str, output)) + '\n'
            outs.append(tmp)
            if len(outs) > 10**5:
                _o.writelines(outs)
            #print cs, rs, c, r, prs[r, c]
            #print rs, cs, r, c, prs.shape
            #print rs, cs, prs[r, c], pearsonr(data_row[r], data_row[c])[0]
        if outs:
            _o.writelines(outs)

    _o.close()

    #print 'finish', i, r, c

if __name__ == '__main__':
    main()
