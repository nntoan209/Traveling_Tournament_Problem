import random # Randomize the team to consider each time

def read_file(path):
    with open(path, "r") as f:
        N = int(f.readline())
    
        d = [[int(x) for x in f.readline().split()] for i in range(N)]
        return N, d


def initialization(N):
    teams = []
    for i in range(N):
        teams.append({})
        teams[i]['distance'] = 0
        teams[i]['pitches'] = [j for j in range(N) if j != i] # Team pitches
        teams[i]['pitches'] += [i for j in range(N - 1)]
        teams[i]['actual_position'] = [i]
        random.shuffle(teams[i]['pitches'])
    return teams


def inside(pitches, closed): # Check if all the elements in closed are inside pitches or not
    for i in pitches:
        if i not in closed:
            return False
    return True


def solve(teams, N, d, considering_team):
    global min_total_distance, teams_data_min # Save the minimum total distance and the corresponding schedule
 
    if len(considering_team) == 0: # If there are no team left to consider for this week
        if len(teams[0]['pitches']) == 0: # If there are no pitch to go for teams[0]
            
            sum = 0 # Calculate the sum of distance of all the teams
            
            for i in range(N):
                sum += teams[i]['distance']
            
            if min_total_distance > sum: # Save the optimal value
                min_total_distance = sum
                teams_data_min = teams
            
            return "Found"
        else:
            considering_team = [i for i in range(N)]
            random.shuffle(considering_team) # Random the next team that we want to consider
    
    a = considering_team[0] # Take the first team in the considering_team list
    closed = [] # Save the team from that we can't find solutions
    
    while inside(teams[a]['actual_position'], closed) == False: 
        min1 = float("inf")
        min2 = float("inf")
        id_min = N
        check = False
        
        for i in teams[a]['pitches']: 
            tmp1 = teams[a]['actual_position'][-1] # The last position of teams[a]
            if i in considering_team and i not in closed: 
                if i == a: # If i is a
                    for j in teams[a]['pitches']: 
                        tmp2 = teams[j]['actual_position'][-1] # The last position of teams[j]
                        if j in considering_team and j != i and tmp2 != i and (a in teams[a]['pitches']) and (a in teams[j]['pitches']):
                            if d[tmp1][i] + d[tmp2][i] < min1 + min2:
                                check = True
                                min1 = d[tmp1][i]
                                min2 = d[tmp2][i]
                                id_min = j
                else:
                    # If the last position of teams[a] is not i and i is not in the pitches where teams[i] must go
                    if tmp1 != i and (i in teams[i]['pitches']): 
                        tmp2 = teams[i]['actual_position'][-1] # The last position of teams[i]
                        
                        # Check the total min distance (from last position of teams[a] to pitch i and from last position of teams[i] to pitch i)
                        if d[tmp1][i] + d[tmp2][i] < min1 + min2: 
                            check = False
                            min1 = d[tmp1][i]
                            min2 = d[tmp2][i]
                            id_min = i
        
        if id_min < N:
            if check == False:
                m = id_min
                n = a
            else:
                m = a
                n = id_min
            
            #Update variables
            teams[a]['actual_position'].append(m) # Update the next position of teams[a]
            teams[id_min]['actual_position'].append(m) # Update the next position of teams[id_min]
            teams[a]['distance'] += min1 # Update the total distance of teams[a]
            teams[id_min]['distance'] += min2 # Update the total distance of teams[id_min]
            teams[a]['pitches'].remove(m) # Remove m from the next pitches to go of teams[a]
            teams[id_min]['pitches'].remove(m) # Remove m from the next pitches to go of teams[id_min]
            
            # Remove m, n from the considering_team list
            considering_team.remove(n) 
            considering_team.remove(m)
            
            # Check if we can generate the next case or not
            if solve(teams.copy(), N, d, considering_team) == "Found":
                return "Found"
            else:
                # Redefine variable - backtrack
                teams[a]['actual_position'].pop()
                teams[id_min]['actual_position'].pop()
                teams[a]['distance'] -= min1 
                teams[id_min]['distance'] -= min2
                teams[a]['pitches'].append(m)
                teams[id_min]['pitches'].append(m)
                
                considering_team.append(n)
                considering_team.append(m)
                
                closed.append(m) # Append m to the closed list - we can't go further after considering m
        else:
            break # and return "Not Found" - no way to go further
    return "Not Found"


path = 'Fundamentals of Optimization/Data/data4/ttp4_1.txt'
N, d = read_file(path) # Read from file
considering_team = [i for i in range(N)] # All the teams need to be paired in one week
teams_data_min = None # Save the optimal schedule
min_total_distance = float("inf") # Save the optimal value

# Loop over 10000 random initializations of teams, hope that we can find optimal value

for c in range(10000):
    teams = initialization(N)
    solve(teams, N, d, considering_team)
print(min_total_distance)

# Print teams_data_min
for i in teams_data_min:
    print(i)