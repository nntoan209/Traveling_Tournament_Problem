import random as rd

def generate(filename, n):
    d = [[0 for j in range(n)] for i in range(n)]    #Creating a (n x n) symmertric matrix
    for i in range(n):
        for j in range(n):
            if i < j:
                d[i][j] = rd.randint(1, 10)   #The distance between any 2 teams is between 1 and 10
            elif i > j:
                d[i][j] = d[j][i]
    with open(filename, 'w') as f:   #Write the data into the file
        f.write(str(n) + '\n')
        for i in range(n):
            for j in range(n):
                f.write(str(d[i][j]) + ' ')
            f.write('\n')
            
for n in range(4, 11, 2):   #The number of teams is 4, 6, 8, 10
    for i in range(1, 51):   #For each number of teams, generate 50 data file
        filename = f'Data/data{n}/ttp{n}_{i}.txt'
        generate(filename, n)