import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#Ford-Fulkerson Algorithm

#visit nodes of the graph using BFS, find path 
def bfs(C, F, s, t):
        stack = [s]
        paths={s:[]}
        if s == t:
                return paths[s]
        while(stack):
                u = stack.pop()
                for v in range(len(C)):
                    #u and v are pointers to each node in graph
                        if(C[u][v]-F[u][v]>0) and v not in paths:
                        #if ther exists a path from u to v where v is not visited
                        #and flow can be passed through
                                paths[v] = paths[u]+[(u,v)]
                                #u is the parent of v so v becomes u
                                #print(paths)
                                if v == t:
                                    #if visited sink node
                                        return paths[v]
                                stack.append(v)
        return None

def max_flow(C, s, t):
        n = len(C) # C is the adjacency matrix
        F = [[0] * n for i in range(n)]
        path = bfs(C, F, s, t)
        #find shortest path
        while path != None:
            #while there is a path
            flow = min(C[u][v] - F[u][v] for u,v in path)
            #find smallest value that can be passed through path
            for u,v in path:
                F[u][v] += flow
                #add pathflow from elements in opp directions for residual
                F[v][u] -= flow
                #subtracting minimum pathFlow from given path 
            path = bfs(C,F,s,t)
        return sum(F[s][i] for i in range(n))



#reads adjacency matrix from a text file and creates matrix for max_flow()
def readMTX(filename):

        #sets up variable
        mTx = []
        size = 0
        mTxFinal = []
        colNum = 0
        rowNum = 0

        #opens .txt file
        f = open(filename, "r")

        #puts .txt file into a matrix split by spaces
        for line in f:
          words = line.split()
          mTx.append(words)
          size = size + 1

        #makes and formates the matrix that will be passed to max_flow()
        for i in range(size - 1):
          colNum += 1
          rowNum = 0
          #sets up a sub matrix for each row to be added to the final matrix
          submTx = []
          for j in range(size):
            #we ignore the letters in the file      
            if rowNum == 0:
                rowNum += 1
            #if we are at the end of the row...
            elif rowNum == 4:
                edge = mTx[colNum][rowNum]
                edgeNum = int(edge)
                #we add the sub matrix into the final matrix
                submTx.append(edgeNum)
                mTxFinal.append(submTx)
                rowNum += 1
            #if we are in any other row 
            else:
                #adds the info into the sub matrix
                edge = mTx[colNum][rowNum]
                edgeNum = int(edge)
                submTx.append(edgeNum)
                rowNum += 1
                
        #returns the final matrix and the size of the matirx - 2 for the sink node.
        return mTxFinal, size - 2



def main():
        #the source node in the .txt file should always be the first node.
        source = 0  # A
        #name of the .txt file 
        filename = "GraphTxt.txt"
        #gets the graph made by the .txt files adjacency matrix
        graph, sink = readMTX(filename)
        #gets the maxflow of the graphAGT
        max_flow_value = max_flow(graph, source, sink)
        print("Ford-Fulkerson algorithm")
        result = "Maxflow value is: ", max_flow_value
        G = nx.from_numpy_array(np.matrix(graph), create_using=nx.DiGraph)
        #use numpy to convert to networkx matrix, add directions
        layout = nx.spectral_layout(G)
        #networkx layout, "Position nodes using the
        #eigenvectors of the graph Laplacian."
        nx.draw(G, layout, node_size=500, with_labels=True,
                font_weight='bold',font_size=15)
        labels = nx.get_edge_attributes(G,'weight')
        #get edge weights
        nx.draw_networkx_edge_labels(G,pos=layout,edge_labels=labels)
        #draw labels
        plt.text(0.2, 0.9,result, fontsize = 12, 
         bbox = dict(facecolor = 'red', alpha = 0.5))
        #show maxflow in plot
        plt.show()
main()

        
