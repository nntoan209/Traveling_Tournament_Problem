def input(filename):
    with open(filename) as f:
        n = int(f.readline())
        d = []
        for i in range(n):
            row = [int(x) for x in f.readline().split()]
            d.append(row)
    return n, d
directory = 'Fundamentals of Optimization/Data/data4/ttp4_'
from ortools.linear_solver import pywraplp
import time

res = []

for i in range(1, 2):
    filename = directory + str(i) + '.txt'
    n, d = input(filename)
    solver = pywraplp.Solver.CreateSolver('CBC')
    INF = solver.infinity()
    t1 = time.time()
    
    #Create variables
    # x(i, j, t) = 1 <=> team i plays at team j in time slot t
    x = [[[solver.IntVar(0, 1, f'x({i}, {j}, {t})') for t in range(1, 2*n-2+1)] for j in range(1, n+1)] for i in range(1, n+1)]

    # y(i, j, t) = 1 <=> team i plays at location j in time slot t
    y = [[[solver.IntVar(0, 1, f'y({i}, {j}, {t})') for t in range(1, 2*n-2+1)] for j in range(1, n+1)] for i in range(1, n+1)]

    # z(i, i1, i2, t) = 1 <=> team i travels from location i1 to i2 between time slots t and t + 1 
    z = [[[[solver.IntVar(0, 1, f'z({i}, {i1}, {i2}, {t})') for t in range(1, 2*n-1+1)] for i2 in range(1, n+1)] for i1 in range(1, n+1)] for i in range(1, n+1)]

    #Constraints
    #No team plays againts itself
    for i in range(1, n+1):
        for t in range(1, 2*n-2+1):
            cstr = solver.Constraint(0, 0)
            cstr.SetCoefficient(x[i-1][i-1][t-1], 1)

    #Team i plays againts only 1 team in each time slot
    for i in range(1, n+1):
        for t in range(1, 2*n-2+1):
            cstr = solver.Constraint(1, 1)
            for j in range(1, n+1):
                cstr.SetCoefficient(x[i-1][j-1][t-1], 1)
                cstr.SetCoefficient(x[j-1][i-1][t-1], 1)
                
    #Team i plays at team j exactly once 
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                cstr = solver.Constraint(1, 1)
                for t in range(1, 2*n-2+1):
                    cstr.SetCoefficient(x[i-1][j-1][t-1], 1)
                    
    #Relation between x and y
    for i in range(1, n+1):
        for j in range(1, n+1):
            for t in range(1, 2*n-2+1):
                if i != j:
                    cstr = solver.Constraint(0, 0)
                    cstr.SetCoefficient(y[i-1][j-1][t-1], 1)
                    cstr.SetCoefficient(x[i-1][j-1][t-1], -1)
                else:
                    cstr = solver.Constraint(0, 0)
                    cstr.SetCoefficient(y[i-1][i-1][t-1], 1)
                    for k in range(1, n+1):
                        cstr.SetCoefficient(x[k-1][i-1][t-1], -1)
                        
    #Relation between y and z
    for i in range(1, n+1):
        for i1 in range(1, n+1):
            for i2 in range(1, n+1):
                for t in range(1, 2*n-3+1):
                    cstr = solver.Constraint(-1, INF)
                    cstr.SetCoefficient(z[i-1][i1-1][i2-1][t-1], 1)
                    cstr.SetCoefficient(y[i-1][i1-1][t-1], -1)
                    cstr.SetCoefficient(y[i-1][i2-1][t+1-1], -1)

    #Objective
    obj = solver.Objective()
    for i in range(1, n+1):
        for i1 in range(1, n+1):
            for i2 in range(1, n+1):
                for t in range(1, 2*n-3+1):
                    obj.SetCoefficient(z[i-1][i1-1][i2-1][t-1], d[i1-1][i2-1])
    for i in range(1, n+1):
        for j in range(1, n+1):
            obj.SetCoefficient(y[i-1][j-1][1-1], d[i-1][j-1])
    obj.SetMinimization()

    #Solve
    rs = solver.Solve()
    t2 = time.time()
    for t in range(1, 2*n-2+1):
        print(f'Week {t}:')
        for i in range(1, n+1):
            for j in range(1, n+1):
                if x[i-1][j-1][t-1].solution_value() == 1:
                    print(f'Team {i} play againts team {j} at the stadium of {j}')
        print()
    print('Optimal objective value =', solver.Objective().Value())
    
    res.append((solver.Objective().Value(), t2-t1))

print(res)