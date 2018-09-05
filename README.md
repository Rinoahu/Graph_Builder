# Graph_Builder
Graph_Builder builds the graph from RNA-seq data. It reads the RNA-seq expression file in tab-delimited format and computes the pairwise pearson correlation matrix. The algorithm of Graph_Builder is a naive method which computes all-vs-all pearson correlation coefficients. The complexity of the algorithm is O(n^3). However, due to the MKL blas library, Graph_Builder runs very fast. In our tests, it took less than 1.5 hour to finish analysis of a RNA-seq data that contains ~180,000 transcripts and ~5,000 samples. The correlation matrix is stored in a triple column format and can be used as input of Markov Clustering Algorithm.
## Requirement

Make sure that you have the following installed

1. Python2.7 (Recommend [Anaconda](https://www.continuum.io/downloads#linux "https://www.continuum.io/downloads#linux" ))
    1. [numpy](http://www.numpy.org/ "http://www.numpy.org/")
    2. [scipy](https://www.scipy.org/ "https://www.scipy.org/")

    3. Install dependency packages via pip:

        $ pip install scipy numpy

    4. Install dependency packages via conda:

        $ conda install scipy numpy


## Download

    $ git clone https://github.com/Rinoahu/Graph_Builder

## Usage

    $python rna_seq/naive_cluster.py -i foo.tab -t .2 -o foo.xyz

-i:   str. The name of a tab-delimited file. The 1st column stand for gene names/identifier and the rest columns stand for gene expression levels in different samples. For example: 

	#id	s1	s2	s3	...
    g1	1.2	2.4	1.2 ...
    g2	1.1	1.2	0 ...
	g3	1.2	1.2	2.2 ...
	...

-t: float. A threshold value to filter low-correlation genes. If the pearson correlation coefficient between gene i and j is less than the threshold, then, it will be set to 0. Default value is 0.2.

-o:   str. The name of output file. The output is an 3 columns tab-delimited file where the 1st and 2nd columns stand for the gene identifiers, the 3rd column is the pearson's correlation coefficient.

