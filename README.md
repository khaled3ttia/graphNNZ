### By: Khaled Abdelaal
khaled.abdelaal@ou.edu

# graphNNZ
A simple tool to count non-zero patterns of a given size in a given graph represented in an adjacency matrix format


The tool takes as input a combined graph file from the SNAP graph dataset and produces a text file containing the count of 2^n possible patterns of zeros and non-zeros for a given vector of size n 

#### Sample usage

        python graphNNZ.py --input data/facebook\_combined.txt --vsize 4 --no-rename > outputfile.out

Also, you can simply run `run.sh` which runs 3 sample datasets with appropriate flags as follows:
        ./run.sh

### Available options

`--input <filepath>` : specifies the input file path.

`--vsize <int>` : specifies the vector size for which patterns will be matched. For example, if `--vsize 4` was used, 2^4 different patterns on the format `1 1 1 1` - `0 0 0 0` will be matched and compared against each 4 consecutive elements of each row of the generated adjaceny matrix.

`--directed` : instructs the script to treat input graph file as a directed graph
`--undirected` : (optional) instructs the script to treat input graph as an undirected graph. If neither `--directed` nor `--undirected` are specified, the default is undirected.

`--rename` : (optional) instructs the script to rename vertices, if the are initially random, unordered numbers. This is `True` by default (even if not specified).

`--no-rename` : instructs the script to skip renaming vertices. 


