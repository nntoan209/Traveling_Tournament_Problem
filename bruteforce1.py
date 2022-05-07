# ----------------------------------------data------------------------------------------#
def get_input(filename):
    cost = []
    with open(filename) as f:
        N =  [int(x) for x in f.readline().split()][0]
        for i in range(N):
            a = [int(x) for x in f.readline().split()]
            cost.append(a)
    return N,cost

N,cost_matrix = get_input('Fundamentals of Optimization/TTP6.inp')

count = 0
played = [False] * (N)
current_pos = [x for x in range(N)]
pre_pos = [x for x in range(N)]
travel = [0 for _ in range(N)] 
remainning_matches = []
Team =[x for x in range(N)]

for i in range(N):
    tmp = [i]*(N-2)
    for j in range(N):
        tmp.append(j)
    remainning_matches.append(tmp)

#-------------------------------------------- one-week ----------------------------------------------------#



def check(rs,temp):
    for i in rs:
        if temp == i[0]:
            return False
    return True

def backtrack(n,remainning_matches,rs = [],tmp = set()):
    if n == 0:
        temp = sorted(list(tmp),key = lambda x : x[0])        
        if check(rs,temp):
            rs.append((temp,sum(travel)))

    else:
        for team in Team:
            if played[team] == False and team in remainning_matches[team]:
                played[team] = True
                n -= 2
                for enemy in Team:
                    if enemy != team and team in remainning_matches[enemy] and played[enemy] == False:
                        played[enemy] = True
                        
                        travel[enemy] += cost_matrix[current_pos[enemy]][team]
                        travel[team] += cost_matrix[current_pos[team]][team]
                        
                        remainning_matches[team].remove(team)
                        remainning_matches[enemy].remove(team)
                        
                        pre_pos[team] = current_pos[team]
                        pre_pos[enemy]= current_pos[enemy]
                        
                        current_pos[team] = team
                        current_pos[enemy]= team
                        
                        tmp.add((team,enemy))
                        backtrack(n,remainning_matches,rs,tmp)
                        
                        tmp.discard((team,enemy))
                        played[enemy] = False
                        
                        remainning_matches[enemy].append(team)
                        remainning_matches[team].append(team)
                        
                        current_pos[enemy] = pre_pos[enemy]
                        current_pos[team] = pre_pos[team]
                        
                        travel[team] -= cost_matrix[current_pos[team]][team]
                        travel[enemy] -= cost_matrix[current_pos[enemy]][team]
                    
                n += 2
                played[team] = False
    return rs

# ------------------------------------------------- all-week-----------------------------------------------#

def find_sum():
    pass

f_opt = float('inf')
solution = None
f_recent = 0
m = 0

def find_all(N,k =0,res = [],tmp = []):
    global f_opt,solution,f_recent,m
    m += 1
    if k == 2 *N -2:
        if f_recent < f_opt:
            f_opt = f_recent
            solution = list(res)
    
    else:
        k += 1
        rs = backtrack(N,remainning_matches,rs = list())
        for week in rs:
            matches, travel = week
            f_recent += travel
            res.append(matches)
            for match in matches:
                host,enemy = match
                
                pre_pos[host] = current_pos[host]
                pre_pos[enemy] = current_pos[enemy]
                
                current_pos[host]= host
                current_pos[enemy] = host
                
                remainning_matches[host].remove(host)
                remainning_matches[enemy].remove(host)
                
            find_all(N,k)
            
            res.pop(-1)
            f_recent -= travel
            for match in matches:
                host,enemy = match
                
                current_pos[host] = pre_pos[host]
                current_pos[enemy] = pre_pos[enemy]
                
                remainning_matches[host].append(host)
                remainning_matches[enemy].append(host)
        k -= 1
    return solution, f_opt



league, cost = find_all(N)   
print('The optimal solution is:', cost)
k = 0
for matches in league:
    k += 1
    print('Week {}'.format(k))
    for match in matches:
        host,enemy = match
        print('Team {} and {} play at the stadium {}'.format(host,enemy,host))
    print()

print(m)