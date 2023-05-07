import State

class ATM:
    def __init__(self) :
        self.cur_state = State.IdleState()

    def insert_card(self, card_info):
        try :
            new_state = self.cur_state.insert_card(card_info)
        except Exception as e:
            print(e)
            return 
        self.cur_state = new_state

    def enter_pin(self,pin):
        try :
            new_state = self.cur_state.enter_pin(pin)
        except Exception as e:
            print(e)
            return 
        self.cur_state = new_state

    def select_account(self):
        self.cur_state = self.cur_state.select_account()

    def see_balance(self):
        self.cur_state = self.cur_state.see_balance()

    def deposit(self,amount):
        self.cur_state = self.cur_state.deposit(amount)

    def withdraw(self,amount): 
        try :     
            new_state = self.cur_state.withdraw(amount)
        except Exception as e:
            print(e)
            return 
        self.cur_state = new_state

    def cancel(self):
        self.cur_state = self.cur_state.cancel()

    def eject_card(self):
        self.cur_state = self.cur_state.eject_card()