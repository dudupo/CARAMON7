import numpy as np 


def buildeq_system(users : int):
    edges = users**2
    eq_system = np.zeros( (users, edges) )
    for i in range(users):
        for j in range(users):
            eq_system[i][j + i*users] +=  1
            eq_system[i][i + j*users] += -1
    return eq_system

def solve(users : int, payments : list):
    payments    = np.array(payments).astype(np.float64)
    payments    -= sum(payments) / users
    solution    = np.linalg.pinv(buildeq_system(users)) @ payments
    return solution.reshape(users,users)

def test():
    print(solve(2, [10,0]))
    print(solve(3, [10,4,11]))
if __name__ == "__main__":
    test()    

