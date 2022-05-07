def input(filename):
    with open(filename) as f:
        n = int(f.readline())
        d = []
        for i in range(n):
            row = [int(x) for x in f.readline().split()]
            d.append(row)
    return n, d
filename = 'Fundamentals of Optimization/Data/data4/ttp4_1.txt'
n, d = input(filename)

from ortools.sat.python import cp_model
model = cp_model.CpModel()

class VarAraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = 1
        
    def on_solution_callback(self):
        self.__solution_count += 1
        print(f'Solution #{self.__solution_count}:')
        for t in range(1, 2*n-2+1):
            print(f'Week {t}:')
            for i in range(1, n+1):
                for j in range(1, n+1):
                    if self.Value(x[i-1][j-1][t-1]) == 1:
                        print(f'Team {i} plays againts team {j} at the stadium of {j}')
            print()
        print('OBJECTIVE VALUE =', self.Value(cp_model.LinearExpr.ScalProd(obj_var, obj_coefficient)))
        print('_____________________________________________________')
        # if self.__solution_count >= self.__solution_limit:
        #     self.StopSearch()
    def solution_count(self):
        return self.__solution_count

#Create Variables:
# x(i, j, t) = 1 <=> team i plays at team j in time slot t
x = [[[model.NewIntVar(0, 1, f'x({i}, {j}, {t})') for t in range(1, 2*n-2+1)] for j in range(1, n+1)] for i in range(1, n+1)]

# y(i, j, t) = 1 <=> team i plays at location i in time slot t
y = [[[model.NewIntVar(0, 1, f'y({i}, {j}, {t})') for t in range(1, 2*n-2+1)] for j in range(1, n+1)] for i in range(1, n+1)]

# z(i, i1, i2, t) = 1 <=> team i travels from location i1 to i2 between time slots t and t + 1 
z = [[[[model.NewIntVar(0, 1, f'z({i}, {i1}, {i2}, {t})') for t in range(1, 2*n-1+1)] for i2 in range(1, n+1)] for i1 in range(1, n+1)] for i in range(1, n+1)]

#Constraint
#No team plays againts itself
for i in range(1, n+1):
    for t in range(1, 2*n-2+1):
        model.Add(x[i-1][i-1][t-1] == 0)
        
#Team i plays againts only 1 team in each time slot
for i in range(1, n+1):
    for t in range(1, 2*n-2+1):
        a = []
        for j in range(1, n+1):
            a.append(x[i-1][j-1][t-1])
            a.append(x[j-1][i-1][t-1])
        model.Add(sum(a) == 1)
        
#Team i plays at team j exactly once 
for i in range(1, n+1):
    for j in range(1, n+1):
        if i!= j:
            a = []
            for t in range(1, 2*n-2+1):
                a.append(x[i-1][j-1][t-1])
            model.Add(sum(a) == 1)
            
#Relation between x and y
for i in range(1, n+1):
    for j in range(1, n+1):
        for t in range(1, 2*n-2+1):
            if i != j:
                model.Add(y[i-1][j-1][t-1] == x[i-1][j-1][t-1])
            else:
                a = []
                for k in range(1, n+1):
                    a.append(x[k-1][i-1][t-1])
                model.Add(y[i-1][i-1][t-1] == sum(a))

#Relation between y and z       
for i in range(1, n+1):
    for i1 in range(1, n+1):
        for i2 in range(1, n+1):
            for t in range(1, 2*n-3+1):
                model.Add(z[i-1][i1-1][i2-1][t-1] >= y[i-1][i1-1][t-1] + y[i-1][i2-1][t+1-1] - 1)     

#Objective
first_time_slot = []
first_time_slot_coefficient = []
for i in range(1, n+1):
    for j in range(1, n+1):
        first_time_slot.append(y[i-1][j-1][1-1])
        first_time_slot_coefficient.append(d[i-1][j-1])
        
remaining = []
remaining_coefficient = []
for i in range(1, n+1):
    for i1 in range(1, n+1):
        for i2 in range(1, n+1):
            for t in range(1, 2*n-3+1):
                remaining.append(z[i-1][i1-1][i2-1][t-1])
                remaining_coefficient.append(d[i1-1][i2-1])

obj_var = first_time_slot + remaining
obj_coefficient = first_time_slot_coefficient + remaining_coefficient
model.Minimize(cp_model.LinearExpr.ScalProd(obj_var, obj_coefficient))

#Solve
solver =cp_model.CpSolver()
solver.parameters.search_branching = cp_model.FIXED_SEARCH
solver.parameters.max_time_in_seconds = 5400                         #Adjust time limit 
solution_printer = VarAraySolutionPrinter(x)
solver.Solve(model, solution_printer)
print(f'OPTIMAL OBJECTIVE VALUE = {solver.ObjectiveValue()}')