from Exceptions import InvalidOperationError, InvalidValueError,InsufficientBalanceError
from Card import Card
from Account import Accounts


class State :
    def insert_card(self, card_info):
        raise InvalidOperationError("Invalid operation: Card already inserted")  
    def enter_pin(self, pin):
        raise InvalidOperationError("Invalid operation: PIN entry not allowed")
    def select_account(self):
        raise InvalidOperationError("Invalid operation: Account selection not allowed")
    def see_balance(self):
        raise InvalidOperationError("Invalid operation: Balance inquiry not allowed")
    def deposit(self,amount):
        raise InvalidOperationError("Invalid operation: Deposit not allowed")
    def withdraw(self,amount):
        raise InvalidOperationError("Invalid operation: Withdrawal not allowed")
    def cancel(self):
        raise InvalidOperationError("Invalid operation: Cancel not allowed")
    def eject_card(self):
        raise InvalidOperationError("Invalid operation: Card not inserted")
   

class IdleState(State):
    def insert_card(self, card_info):
        card_number = card_info['card_number']
        if not self._check_isvalid(card_number):
            raise InvalidValueError("Invalid Card")
        
        my_card = Card(card_info)
        return CardInsertedState(my_card)
    
    def _check_isvalid(self, card_number):
        #check card_number is invalid
        #Add a check code if there is a card number pattern available at this atm.
        #I just add a pattern
        return card_number[0] == '1'    
    
class CardInsertedState(State):
    def __init__(self, card):
        self.card = card

    def enter_pin(self, pin):
        if not self._check_isvalid(pin):
            raise InvalidValueError("Invalid PIN number: Please check your pin number")
        return SelectAccountState(card=self.card)
      
    def _check_isvalid(self, pin):
        return self.card.pin == pin
    
    def cancel(self):
        return EjectCardState()

class SelectAccountState(State):
    def __init__(self, db_file = 'accounts.txt', card = None):
        self.cur_account = None 
        self.accounts = Accounts(db_file) 
        self.cur_card = card

    def select_account(self):
        self.cur_account = self._get_account()
        '''
        It was specified that the part to select the account was necessary, 
        so I made function for this
        but if conditions are added later, we can add here.

        However, since the current condition is unknown,
        Therefore It just goes to the next state.
        '''
        return TransactionState(self.cur_account)
    
    def _get_account(self):
        '''
        I assume that if the card is valid for that atm,
        this account also exists in the account list.
        '''
        card_num = self.cur_card.card_number
        return self.accounts.get_account(card_num)
            
    def cancel(self):
        return EjectCardState()
    
class TransactionState(State):
    def __init__(self, account):
        self.selected_account = account
        self.cur_balance = -1  #for test 
        
    
    def see_balance(self):
        self.cur_balance = self.selected_account.get_balance()
        print(self.selected_account.get_balance())
        return self

    def deposit(self,amount):
        self.selected_account.deposit(amount)
        return self
    
    def withdraw(self,amount):
        if self.selected_account.withdraw(amount):
            return self
        raise InsufficientBalanceError()
    
    def cancel(self):
        return EjectCardState()
    
class EjectCardState(State):
    def eject_card(self):
        print("Eject card")
        return IdleState()
    


    
