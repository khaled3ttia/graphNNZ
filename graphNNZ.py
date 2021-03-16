'''
    By: Khaled Abdelaal
    khaled.abdelaal@ou.edu
'''

import argparse
import itertools

def parseGraph(graphFile, directed=False, rename=False):
    adjacencyDict = {}
    nameMap = {}

    i = 0
    maxDim = 0
    numEdges = 0 
    
    with open(graphFile, 'r') as gfile:
        for line in gfile:
            
            nodeList = line.rstrip().split()
            # parse the src and destination nodes
            srcNode = int(nodeList[0])
            dstNode = int(nodeList[1])

            # If renaming is enabled, do it!
            if rename:
                if srcNode not in nameMap:
                    nameMap[srcNode] = i
                    i += 1
                if dstNode not in nameMap:
                    nameMap[dstNode] = i
                    i += 1
                srcNode = nameMap[srcNode]
                dstNode = nameMap[dstNode]
            
            # We need also the maximum node index 
            # to build the adjacency matrix later
            if srcNode > maxDim:
                maxDim = srcNode
            if dstNode > maxDim:
                maxDim = dstNode

            # Append dstNode to the list of srcNode adjacents
            if srcNode not in adjacencyDict:
                adjacencyDict[srcNode] = []
            adjacencyDict[srcNode].append(dstNode)
            numEdges += 1 

            # If the graph is undirected, we need to add another
            # entry for the destination node as well
            # For example: if we have A B
            # Then we need to have B in the adjacency list of A
            # and A in the adjacency list of B
            if (not directed):
                if dstNode not in adjacencyDict:
                    adjacencyDict[dstNode] = []
                adjacencyDict[dstNode].append(srcNode)
                numEdges += 1 

    print(f"numEdges: {numEdges}")

    return adjacencyDict, (maxDim,numEdges)



def newCountPatterns(graphDict, maxDim,  vectorSize = 4):
    print(f'Pattern Matching vector size is:{vectorSize}')
    counterDict = {}
    for k in graphDict:
        currentRow = graphDict[k]
        currentDenseRow = [1 if x in currentRow else 0 for x in range(0, maxDim)]
        j = 0  
        while(j < maxDim):
            if currentDenseRow[j] == 0:
                j += 1 
                continue
            else:
                if maxDim - j < vectorSize:
                    j = maxDim - vectorSize
                start = currentDenseRow[j]
                currentSlice = currentDenseRow[j:j+vectorSize]
                patt = [1 if x == 1 else 0 for x in range(vectorSize)]
                
                for comb in itertools.product([1,0], repeat=vectorSize):
                    pattString = ' '.join([str(elem) for elem in list(comb)])
                    if (list(comb) == currentSlice):
                        if (not pattString in counterDict):
                            counterDict[pattString] = 0 
                        counterDict[pattString] += 1 
                        break
                j += vectorSize

    sorted_counter = {k: v for k,v in sorted(counterDict.items(), key=lambda item: item[1], reverse=True)}
    
    return sorted_counter

def analyzeCount(counterDict, totalNNZ):
    
    for k in counterDict:
        intK = [int(x) for x in k.split()]
        onesCount = 0 
        for j in intK:
            if j == 1: 
                onesCount += 1
        nnzCoverage = onesCount * counterDict[k]
        nnzPercentage = (nnzCoverage / totalNNZ) * 100
        print(f"{k} : {counterDict[k]} : {nnzCoverage} : {nnzPercentage: .2f}%")

def countPatterns(inputMat, vectorSize = 4):

    patterns = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 10:[]}
    counter = {}
    vectorSize = 4
    #for comb in itertools.combinations_with_replacement([0,1], 4):
    for comb in itertools.product([0,'x'],repeat=vectorSize):
        patt = list(comb)
        nnz = 0
        for item in patt:
            if item != 0:
                nnz += 1
        pnnz = nnz / vectorSize
        if pnnz >= 0.95:
            priority = 1
        elif pnnz >= 0.9:
            priority = 2
        elif pnnz >= 0.85:
            priority = 3
        elif pnnz >= 0.8:
            priority = 4
        elif pnnz >= 0.75:
            priority = 5
        elif pnnz >= 0.7:
            priority = 6
        elif pnnz >= 0.6:
            priority = 7
        elif pnnz >= 0.5:
            priority = 8
        else:
            priority = 10

        patterns[priority].append(patt)
        pattString = ' '.join([str(elem) for elem in patt])
        counter[pattString] = 0

    for i in range(len(inputMat)):
        for j in range(len(inputMat[0])):
            if inputMat[i][j] != 0:
                inputMat[i][j] = 'x'
        matchFound = False
        targetPriority = 1
        while (not matchFound and (targetPriority < 9)):
            for patt in patterns[targetPriority]:
                pattString = ' '.join([str(elem) for elem in patt])
                if inputMat[i] == patt:
                    matchFound = True
                    counter[pattString] += 1
                    break
            targetPriority += 1



    sorted_counter = {k: v for k,v in sorted(counter.items(), key=lambda item: item[1], reverse=True)}
    for key,val in sorted_counter.items():
        print(f"{key} : {val}")


if __name__ == '__main__':
    '''
    inputMat = [[1,2,0,1],
                [5,0,0,0],
                [9,3,0,6],
                [0,1,0,3],
                [9,8,7,0]]

    countPatterns(inputMat, 4)
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input File Path")
    parser.add_argument("--directed", dest='directed', default=False, required=False, action='store_true', help="Directed Graph")
    parser.add_argument("--undirected", dest='directed', default=True, required=False, action='store_false', help="Undirected Graph")

    parser.add_argument("--rename", dest='rename', required=False, default=True, action="store_true", help="Rename vertices")
    parser.add_argument("--no-rename", dest='rename', required=False, default=False, action="store_false", help="Don't rename vertices")

    parser.add_argument("--vsize", dest='vsize', required=False, default=4, help="pattern matching vector size")

    args = parser.parse_args()

    print(f"Parsing Graph File {args.input} as a{' directed' if args.directed else 'n undirected'} graph...\nRenaming vertices is {'ON' if args.rename else 'OFF'}")


    graphDict, (maxDim,numEdges) = parseGraph(args.input, directed=args.directed, rename=args.rename)
    counterDict = newCountPatterns(graphDict, maxDim, vectorSize=int(args.vsize))
    analyzeCount(counterDict, numEdges)
