import random as rd

def input(filename):
    with open(filename) as f:
        n = int(f.readline())
        d = []
        for i in range(n):
            row = [int(x) for x in f.readline().split()]
            d.append(row)
    return n, d
filename = 'Fundamentals of Optimization/TTP/Data/data4/TTP4_1.txt'
n, d = input(filename)

#Calculate the total distance travel from the current position to the next position given by sol
def calculate_distance(position, sol):
    new_position = [None for _ in range(1, n+1)]
    for _pair_ in sol:
        team1 = _pair_[0]
        team2 = _pair_[1]
        new_position[team1-1] = team2
        new_position[team2-1] = team2
    res = 0
    for i in range(1, n+1):
        res += d[position[i-1]-1][new_position[i-1]-1]
    return res

#Updating available pairs for the current week
def update_available_pairs(current_available_pairs, current_solution):
    b = []
    for _pair in current_available_pairs:
        check = 0
        for __pair in current_solution:
            if __pair != None:
                if __pair[0] in _pair or __pair[1] in _pair:
                    check = 1
                    break
        if check == 0:
            b.append(_pair)
    return b

#Greedy algorithm to build the current week
def greedy(k, current_position, available_pairs):    #Build the k-th pair of the current week
    global f_opt
    global x_opt 
    for pair in available_pairs.copy():
        current_week[k-1] = pair
        if k == n/2:    #If we finished finding a feasible solution for the current week
            cost = calculate_distance(current_position, current_week)    #Calculate the cost if we use this solution
            if cost < f_opt:
                f_opt = cost    #Update the minimum cost
                x_opt = current_week.copy()    #Update the solution for the current week
        else:
            c = update_available_pairs(available_pairs.copy(), current_week)    #Update available pairs for the current week
            greedy(k+1, current_position, c)    #Build the k+1-th pair of the current week
        current_week[k-1] = None 

#Randomly choosing the solution for the first week       
def build_first_week():
    res = []
    a = list(range(1, n+1))
    rd.shuffle(a)
    while len(a) > 0:
        res1 = a.pop()
        res2 = a.pop()
        res.append((res1, res2))
    return res

best_objective = float("inf")
best_solution = None
for _ in range(10):     
    solution = [None for _ in range(1, 2*n-2+1)]   #Create an empty solution
    current_position = [i for i in range(1, n+1)]      #Initial position of each team
    obj = 0
    A = []    #Build a set containing all possible pairs of teams
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                A.append((i, j))  
                
    first_week = build_first_week()  #Build a solution for the first week
    solution[0] = first_week
    obj += calculate_distance(current_position, first_week)   #Update the objective value
    for pair in first_week:
        team1 = pair[0]
        team2 = pair[1]
        current_position[team1-1] = team2    #Update position after first week   
        current_position[team2-1] = team2
        A.remove(pair)   #Update available pairs for remaining weeks
    
    for i in range(2, 2*n-2+1):     #Build a solution for 2n-2 weeks
        current_week = [None for _ in range(1, n//2 + 1)]    #Create empty solution for the current week
        f_opt = float("inf")
        x_opt = None
        greedy(1, current_position, A)   #Build the solution for the current week 
        obj += f_opt   
        if x_opt == None:    #If we can't find a feasible solution, break out and build another solution from the beginning
            obj = float("inf")
            break
        solution[i-1] = x_opt.copy()
        for pair in x_opt:
            team1 = pair[0]
            team2 = pair[1]
            current_position[team1-1] = team2    #Update position after the current week
            current_position[team2-1] = team2
            A.remove(pair)     #Update available pairs for remaining weeks
            
    if obj < best_objective:    #Update the best solution so far
        best_objective = obj
        best_solution = solution.copy()
        
#Print the solution         
for k in range(1, 2*n-2+1):
    print(f'Week {k}:')
    for pair in best_solution[k-1]:
        print(f'Team {pair[0]} plays against team {pair[1]} at the stadium of {pair[1]}')
    print()
print(f'Objective Value = {best_objective}')
