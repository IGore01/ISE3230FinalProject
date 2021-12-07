# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:35:51 2021
 
@author: August Slawienski, Cameron Lucas, Ishan Gore
"""
 
import cvxpy as cp
import numpy as np
 
constraints = []

#New variable
# column vector for which nodes we must go to
n = cp.Variable(shape=(16,1), boolean=True)
# variable matrix for which edges we travel
x = cp.Variable(shape=(16, 16), boolean=True)
# variable vector to enforce no subtours
t = cp.Variable(16, nonneg=True)
# constant matrix for distances of each path
c = np.array([[1000, 4, 9, 11, 4, 11, 7, 14, 8, 11, 12, 11, 4, 6, 11, 12],
    [4, 1000, 7, 11, 3, 9, 10, 16, 10, 9, 10, 10, 7, 8, 8, 9],
    [9, 7, 1000, 9, 6, 5, 14, 17, 12, 4, 4, 9, 9, 8, 3, 6],
    [11, 11, 9, 1000, 8, 5, 13, 8, 9, 10, 10, 17, 11, 7, 7, 14],
    [4, 3, 6, 8, 1000, 7, 9, 14, 8, 8, 9, 11, 4, 4, 8, 8],
    [11, 9, 5, 5, 7, 1000, 14, 13, 10, 5, 5, 12, 11, 10, 4, 11],
    [7, 10, 14, 13, 9, 14, 1000, 7, 4, 16, 17, 19, 6, 7, 15, 16],
    [14, 16, 17, 8, 14, 13, 7, 1000, 7, 18, 17, 23, 12, 10, 14, 20],
    [8, 10, 12, 9, 8, 10, 4, 7, 1000, 14, 14, 19, 6, 5, 12, 17],
    [11, 9, 4, 10, 8, 5, 16, 18, 14, 1000, 4, 8, 10, 11, 4, 4],
    [12, 10, 4, 10, 9, 5, 17, 17, 14, 4, 1000, 8, 13, 10, 3, 5],
    [11, 10, 9, 17, 11, 12, 19, 23, 19, 8, 8, 1000, 14, 15, 10, 4],
    [4, 7, 9, 11, 4, 11, 6, 12, 6, 10, 13, 14, 1000, 4, 11, 12],
    [6, 8, 8, 7, 4, 10, 7, 10, 5, 11, 10, 15, 4, 1000, 8, 12],
    [11, 8, 3, 7, 8, 4, 15, 14, 12, 4, 3, 10, 11, 8, 1000, 7],
    [12, 9, 6, 14, 8, 11, 16, 20, 17, 4, 5, 4, 12, 12, 7, 1000]])
 
# constant vector for time at each node
cst = np.array([[3, 9, 3, 3, 7, 12, 5, 6, 3, 3, 5, 4, 2, 7, 10, 3]])

# dictionary to containing ampping of our locations
namesDict = {
    0 : "The Shoe",
    1 : "The RPAC",
    2 : "Browning Ampitheatre/Mirror Lake",
    3 : "Wexner Center for the Arts",
    4 : "Thompson Library",
    5 : "The Union",
    6 : "Fisher College of Business",
    7 : "Northeast Dorms (near Lane and High)",
    8 : "Scott Dining Hall",
    9 : "Kennedy Traditions",
    10 : "Jessie Owens South",
    11 : "Wexner Medical Center",
    12 : "The Numbers Garden",
    13 : "18th Avenue Library",
    14 : "Baker West Dormitory",
    15 : "Marketplace on Neil"
        }

# prompt for time input
time = input("How many minutes do you have for this tour?: ")

extraLocs = []
fullLocs = ["The Union"]
             
print()

loop = '-1'
used = []

# loop to continually prompt for which locations to add as mandatory stops
while loop != "":
    if len(extraLocs) > 0:
        print("Your trip currently includes: " + ', '.join(extraLocs) + ".")
    else:
       print("Your trip currently only includes the mandatory stops.")
    loop = input("Please type the number of the location you would like to make mandatory on your tour (this does not guarantee " +
                 "that your tour is feasible given your time limit). Enter nothing to finish.\n\n" +
                 "1. Wexner Center for the Arts\n2. Fisher College of Business\n3. Northeast Dorms (near Lane and High)\n" +
                 "4. Kennedy Traditions\n5. Jessie Owens South\n6. Wexner Medical Center\n7. The Numbers Garden\n" +
                 "8. 18th Avenue Library\n9. Baker West Dormitory\n10. Marketplace on Neil\n")

    if loop in used:
        print("\nYou already included that one...")
    elif loop == '1':
        extraLocs.append("Wexner Center for the Arts")
        constraints.append(n[3,0] == 1)
    elif loop =='2':
        extraLocs.append("Fisher College of Business")
        constraints.append(n[6,0] == 1)
    elif loop == '3':
        extraLocs.append("Northeast Dorms (near Lane and High)")
        constraints.append(n[7,0] == 1)
    elif loop =='4':
        extraLocs.append("Kennedy Traditions")
        constraints.append(n[9,0] == 1)
    elif loop =='5':
        extraLocs.append("Jessie Owens South")
        constraints.append(n[10,0] == 1)
    elif loop =='6':
        extraLocs.append("Wexner Medical Center")
        constraints.append(n[11,0] == 1)
    elif loop =='7':
        extraLocs.append("The Numbers Garden")
        constraints.append(n[12,0] == 1)
    elif loop =='8':
        extraLocs.append("18th Avenue Library")
        constraints.append(n[13,0] == 1)
    elif loop =='9':
        extraLocs.append("Baker West Dormitory")
        constraints.append(n[14,0] == 1)
    elif loop =='10':
        extraLocs.append("Marketplace on Neil")
        constraints.append(n[15,0] == 1)

    used.append(loop)

# objective is to maximize number of places we visit
obj_func = cp.sum(n)

#Required places to visit
constraints.append(n[0,0] == 1) #The Shoe
constraints.append(n[1,0] == 1) #RPAC
constraints.append(n[2,0] == 1) #Browning Amphitheatre
constraints.append(n[4,0] == 1) #Thompson
constraints.append(n[5,0] == 1) #Union
constraints.append(n[8,0] == 1) #Scott
# constraints.append(n[15,0] == 1) #Marketplace
 
# only take one path (if n=1) to go to a destination
col_sums = cp.sum(x, axis=0, keepdims=True) # axis=0 sums over rows for each column
constraints.append(col_sums.T == n)
# from a destination (given n = 1) only go to one place
row_sums = cp.sum(x, axis=1, keepdims=True) # axis=1 sums over columns for each row
constraints.append(row_sums == n)
 
# constraints to eliminate any subtours
for i in range(15):
    for j in range(15):
        if i != j:
            constraints.append(t[i+1] - t[j+1] + 16*x[i,j] <= 15)
 
# Total time constraint
# total time is time to travel + time spent at location
constraints.append(cp.trace(c@x)+cp.trace(n@cst) <= time) # arbitrary time constraint

# solve problem using GUROBI
problem = cp.Problem(cp.Maximize(obj_func), constraints)
problem.solve(solver=cp.GUROBI,verbose = True)
 
# print our values
print("obj_func =")
print(obj_func.value)
print("x =")
print(x.value)
print("n =")
print(n.value)

# print output message depending on if problem is feasible or not
if (obj_func.value != None):
    nextLoc = int(np.where(x.value[:,5] == 1)[0])

    while nextLoc != 5:
        fullLocs.append(namesDict[nextLoc])
        nextLoc = int(np.where(x.value[:,nextLoc] == 1)[0])

    print()
    print("Your trip will end up visiting the following locations, in order: \n\n" + "\n".join(fullLocs))
else:
    print("\nYou're gonna need more time for that...")

    