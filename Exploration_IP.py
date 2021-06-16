# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:03:56 2020

@author: jfb2444
"""

import time
import numpy as np
import gurobipy as gp
from gurobipy import GRB

def solveExplorationPuzzle(N, netRewards):
          
    # Create a new model
    print("\n-----------------------------")
    print("Building Model: Mars Rover Exploration Puzzle")
    model = gp.Model("ExplorationPuzzle_Model")
    model.Params.OutputFlag = 1
    model.Params.varBranch = 2                  # The default -1 setting makes an automatic choice, depending on problem characteristics. Available alternatives are Pseudo Reduced Cost Branching (0), Pseudo Shadow Price Branching (1), Maximum Infeasibility Branching (2), and Strong Branching (3).
    
    # Define objective function direction
    model.modelSense = GRB.MAXIMIZE

    # Parameters
    Rows = range(0,N)
    Columns = range(0,N)
    Pred = np.empty((N, N), dtype=object)                  
    for i in Rows:
        for j in Columns:
            if i == 0:
                Pred[i][j] = []
            else:
                if j == 0:
                    Pred[i][j] = [0,1]
                elif j == N-1:
                    Pred[i][j] = [N-2,N-1]
                else:
                    Pred[i][j] = [j-1,j,j+1]                   
                    
    # Create variables
    x = model.addVars(Rows, Columns, vtype=GRB.BINARY, obj=netRewards, name="var_CellExploration")
    
    # Define Constraints
    for i in Rows: 
        for j in Columns: 
            for k in Pred[i][j]: 
                model.addConstr( x[i,j] <= x[i-1,k], "ct_Pred[%s,%s,%s]" % (i,j,k) )
                       
    # Solve the model
    print("\nSolving Puzzle")
    start_time = time.time()
    model.optimize()
    runtime = time.time() - start_time
    model.write("ExplorationPuzzle.lp")

    # Postprocessing
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    chosenCells = []
    if status == GRB.INFEASIBLE:
        print("Puzzle is infeasible.") 
    elif status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        objValue = model.objval
        cell_sol = np.empty((N,N))
        print("Solution: \n")      
        print(" ", end="")
        for i in Rows:
            print("----", end ="")
        print("")         
        for i in Rows:
            print("", end =" | ")
            for j in Columns:
                print(abs(round(x[i,j].x)), end =" | ")
                cell_sol[i][j] = abs(round(x[i,j].x))
                if cell_sol[i][j] == 1:
                    tmpTuple = (i,j)
                    chosenCells.append(tmpTuple)
            print()
            print(" ", end="")
            for i in Rows:
                print("----", end ="")
            print("")
            
        return chosenCells, objValue, runtime