import numpy as np


q_table = np.load("Q_table.txt.npy")
for i in range(9) :
    for j in range(16):
        for k in range(4):
            for l in range(24):
                if q_table[i,j,k,l] != 0:
                    print("Index: ", i, " j: ", j , " k: ", k, " l: ",l," Q :",q_table[i,j,k,l])