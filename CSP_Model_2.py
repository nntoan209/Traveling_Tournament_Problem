path = 'Fundamentals of Optimization/Data/data4/ttp4_1.txt'

from ortools.sat.python import cp_model
import numpy as np

M = 999999
model = cp_model.CpModel()

# File open
with open(path, "r") as f:
    N = int(f.readline())
    
    d = [[int(x) for x in f.readline().split()] for i in range(N)]
    max_d = max(max(d))
    min_d = min(min(d))
    d = np.array(d)
    
    X = []
    for k in range(2 * N - 2):
        X.append([])
        for i in range(N):
            X[k].append([])
            for j in range(N):
                X[k][i].append(model.NewIntVar(0, 1, 'Week ' + str(k + 1) + ' : Team ' + str(i + 1) + ' meets team ' + str(j + 1)))
    X = np.array(X)
    
    
    for k in range(2 * N - 2):
        for i in range(N):
            model.Add(X[k,i,i] == 0)
    
    
    for i in range(N):
        for j in range(N):
            if i != j:
                constraint = []
                for k in range(2 * N - 2):
                    constraint.append(X[k,i,j])
                model.Add(sum(constraint) == 1)
    
    
    for k in range(2 * N - 2):
        for i in range(N):
            constraint = []
            for j in range(N):
                constraint.append(X[k,i,j])
                constraint.append(X[k,j,i])
            model.Add(sum(constraint) == 1)
    
    
    cost = []
    for k in range(2 * N - 2):
        cost.append([])
        for i in range(N):
            cost[k].append(model.NewIntVar(min_d * (N - 1), max_d * (2 * N - 2), 'cost[' + str(i + 1) + ']'))
    cost = np.array(cost)
    
    
    for k in range(1, 2 * N - 2):
        for i in range(N):
            model.Add(cost[k,i] >= cost[k - 1,i])
    
    
    for i in range(N):
        for j in range(N):
            model.Add(M * (X[0,i,j] - 1) + cost[0,j] <= d[j,i])
            model.Add(M * (1 - X[0,i,j]) + cost[0,j] >= d[j,i])
    
    
    for k in range(1, 2 * N - 2):
        for j in range(N):
            for i in range(N):
                for i_prime in range(N):
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,j,i_prime] - 1) + cost[k,j] <= cost[k - 1,j] + d[i,j])
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,j,i_prime] - 1) + cost[k,j] <= cost[k - 1,j] + d[i,j])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,j,i_prime]) + cost[k,j] >= cost[k - 1,j] + d[i,j])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,j,i_prime]) + cost[k,j] >= cost[k - 1,j] + d[i,j])
         
          
    for k in range(1, 2 * N - 2):
        for j in range(N):
            for i in range(N):
                for i_prime in range(N):
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,i_prime,j] - 1) + cost[k,j] <= cost[k - 1,j] + d[i,i_prime])
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,i_prime,j] - 1) + cost[k,j] <= cost[k - 1,j] + d[i,i_prime])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,i_prime,j]) + cost[k,j] >= cost[k - 1,j] + d[i,i_prime])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,i_prime,j]) + cost[k,j] >= cost[k - 1,j] + d[i,i_prime])
    
    
    for k in range(1, 2 * N - 2):
        for i in range(N):
            for j in range(N):
                for j_prime in range(N):
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,j_prime,i] - 1) + cost[k,i] <= cost[k - 1,i] + d[i,j_prime])
                    model.Add(M * (X[k-1,i,j] - 1) + M * (X[k,j_prime,i] - 1) + cost[k,i] <= cost[k - 1,i] + d[i,j_prime])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,j_prime,i]) + cost[k,i] >= cost[k - 1,i] + d[i,j_prime])
                    model.Add(M * (1 - X[k-1,i,j]) + M * (1 - X[k,j_prime,i]) + cost[k,i] >= cost[k - 1,i] + d[i,j_prime])
    
    
    model.Minimize(sum(cost[-1]))
    
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal cost: {}'.format(solver.ObjectiveValue()),end = '\n\n')
        for k in range(2 * N - 2):
            print("Week " + str(k + 1) + ": ")
            for i in range(N):
                for j in range(N):
                    if solver.Value(X[k,i,j]) == 1:
                        print("Team {} - team {}".format(i + 1, j + 1))
            print()
    else:
        print('No solution found.')