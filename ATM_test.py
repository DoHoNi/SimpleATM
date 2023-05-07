import unittest
from ATM import ATM
import State

class TestATM(unittest.TestCase):
    def setUp(self):
        self.atm = ATM()
        self.cur_card_info = {'card_number':'1234-5678-1234-5678','pin':'1234'}
        self.cur_balance = 100 

    def test_insert_card(self):
        self.atm.insert_card(self.cur_card_info)
        self.assertIsInstance(self.atm.cur_state, State.CardInsertedState)
        
    def test_enter_pin_correct(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.assertIsInstance(self.atm.cur_state, State.SelectAccountState)

    def test_enter_pin_incorrect(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("0000")
        self.assertIsInstance(self.atm.cur_state, State.CardInsertedState)
        

    def test_select_account(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.atm.select_account()
        self.assertIsInstance(self.atm.cur_state, State.TransactionState)

    def test_view_balance(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.atm.select_account()
        self.assertIsInstance(self.atm.cur_state, State.TransactionState)

    def test_deposit(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.atm.select_account()
        initial_balance = self.atm.cur_state.selected_account.balance
        deposit_amount = self.cur_balance
        self.atm.deposit(deposit_amount)
        self.assertEqual(self.atm.cur_state.selected_account.balance, initial_balance + deposit_amount)

    def test_withdraw_sufficient_balance(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.atm.select_account()
        initial_balance = self.atm.cur_state.selected_account.balance
        withdraw_amount = 50
        self.atm.withdraw(withdraw_amount)
        self.assertEqual(self.atm.cur_state.selected_account.balance, initial_balance - withdraw_amount)
        self.assertIsInstance(self.atm.cur_state, State.TransactionState)

    def test_withdraw_insufficient_balance(self):
        self.atm.insert_card(self.cur_card_info)
        self.atm.enter_pin("1234")
        self.atm.select_account()
        initial_balance = self.atm.cur_state.selected_account.balance
        withdraw_amount = initial_balance + 100  
        self.atm.withdraw(withdraw_amount)
        self.assertIsInstance(self.atm.cur_state, State.TransactionState)
        self.assertEqual(self.atm.cur_state.selected_account.balance, initial_balance)
    

if __name__ == '__main__':
    unittest.main()
