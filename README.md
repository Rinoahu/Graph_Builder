# Graph_Builder
This project contains several high performance tools to build the graph from RNA-seq data. It reads the RNA-seq expression file in tab-delimited format and computes the pairwise pearson correlation matrix.

## Requirement

Make sure that you have the following installed

1. Python2.7 (Recommend [Anaconda](https://www.continuum.io/downloads#linux "https://www.continuum.io/downloads#linux" ))
    1. [numpy](http://www.numpy.org/ "http://www.numpy.org/")
    2. [scipy](https://www.scipy.org/ "https://www.scipy.org/")
    3. [sklearn](http://scikit-learn.org/stable/ "http://scikit-learn.org/stable/")
    4. [numba](https://numba.pydata.org/ "https://numba.pydata.org/")

    5. Install dependency packages via pip:

        $ pip install scipy numpy scikit-learn

    6. Install dependency packages via conda:

        $ conda install scipy numpy scikit-learn


## Download

    $ git clone https://github.com/Rinoahu/Graph_Builder

## Usage

    $python MCL_lite/mcl_sparse.py -i foo.xyz -I 1.5 -o foo.mcl -a 8 -m 8 -d t

-i:   str. The name of a tab-delimited file. The 1st column stand for gene names/identifier and the rest columns stand for gene expression levels in different samples. For example: 

	#id	s1	s2	s3	...
    g1	1.2	2.4	1.2 ...
    g2	1.1	1.2	0 ...
	g3	1.2	1.2	2.2 ...
	...

-t: float. A threshold value to filter low-correlation genes. If the pearson correlation coefficient between gene i and j is less than the threshold, then, it will be set to 0.

-o:   str. The name of output file. The output file is an  N x N pearson correlation matrix, where N is the gene number.

