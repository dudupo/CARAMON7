import argparse
from datetime import datetime
import pickle
import constants
import numpy as np
from eq import solve


from os import system

class User:
    def __init__(self, name : str) -> None:
        self.name = name

class Payment:
    
    def __init__(self, cost : float, title : str, user : User):
        self.date = datetime.now()
        self.cost, self.title, self.user = cost, title, user
    
    def __str__(self):
        return f"{self.title: < 10}\t{self.date.date()}\t{self.cost:<10.6}\t{self.user.name}"

class House:
    def __init__(self) -> None:
        self.users = { name: User(name) for name in constants.USERSNAMEs }
        self.name  = constants.HOUSENAME 
        self.payments_acc_dict = {  user.name : 0 for user in self.users.values() }
        self.payments = []
        
    def payment_commit(self, payment : Payment) -> None:
        self.payments.append(payment)
        self.payments_acc_dict[payment.user.name] += payment.cost

    def status(self) -> str:
        matrix = solve(self.users.keys().__len__(), list(self.payments_acc_dict.values()))
        return str(matrix)
    
def install():
    '''generate pickle databse for the first time'''
    Carmon = House()
    with open(f"{constants.HOUSENAME}.pkl", "wb" ) as pklfile:
        pickle.dump(Carmon, pklfile )
    return Carmon

def loaddecorator(func):
    def inner(*args, **kwards):
        with open(f"{constants.HOUSENAME}.pkl", "rb" ) as pklfile:
            house = pickle.load(pklfile)
        return func( (*args, house), **kwards)
    return inner

def dump(house : House):
    with open(f"{constants.HOUSENAME}.pkl", "wb" ) as pklfile:
        pickle.dump(house, pklfile )
    
def gitpull():
    if constants.GITENABLE:
        system(f"git pull origin main")

def gitpush():
    if constants.GITENABLE:
        system(f"git add {constants.HOUSENAME}.pkl")
        system(f"git commit -m test")
        system(f"git push origin main")

def gitpushdecorator(func):
    def inner(*args, **kwards):
        gitpull()
        ret = func(*args, **kwards)
        gitpush()
        return ret
    return inner 

@loaddecorator
def loadHouse(house):
    return house

@gitpushdecorator
def payment_commit(house):
    house.payment_commit(\
    Payment(float(command[2]), command[1], house.users[args.user]))
    dump(house)

if __name__ == "__main__":

    from pathlib import Path
    pklfile = Path(f"./{constants.HOUSENAME}.pkl")
    if pklfile.is_file():
        house = loadHouse()[0]
    else:
        house = install()
    
    parser = argparse.ArgumentParser(description='Process House Budget.')
    parser.add_argument('--user', type=str,
                        help='user name')
    parser.add_argument('--action', type=str)
    args = parser.parse_args() 

    command = args.action.split()
    if command[0] == "pay":
        payment_commit(house)
    if command[0] == "print":
        print(house.status())
    
    if command[0] == "reset":
        house = install()

