
class Account:
    def __init__(self, card_num , balance=0): 
        self.card_num = card_num 
        self.balance = balance
    
    def get_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
    
    def deposit(self, amount):
        self.balance += amount

#You can get the account information from the server,
#I assume that there is a simple db file and implement it as a simple file reader. 
class Accounts:
    def __init__(self, db_file):
        self.accounts = dict()
        self.db_file = db_file
        self.read_db()

    def read_db(self):
        with open(self.db_file,'r') as f:
            while True:
                line = f.readline()
                if not line :
                    break
                card_num , balance = line.split(',')
                balance = int(balance)
                self.accounts[card_num] = Account(card_num, balance)

    def update(self, card_num, value):
        self.accounts[card_num] = value
    
    def get_account(self,card_num):
        if card_num not in self.accounts:
            return None
        return self.accounts[card_num]