import unittest
import State
import Exceptions
from Account import Account, Accounts
from Card import Card

class TestIdleState(unittest.TestCase):
    def setUp(self):
        self.state = State.IdleState()
        self.card_info = {'card_number':'1234-5678-1234-5678','pin':'1234'}
        self.wrong_card_info = {'card_number':'2234-5678-1234-5678','pin':'1234'}

    def test_insert_card(self):
        next_state = self.state.insert_card(self.card_info)
        self.assertIsInstance(next_state, State.CardInsertedState)

    def test_insert_invalid_card(self):
        with self.assertRaises(Exceptions.InvalidValueError):
            next_state = self.state.insert_card(self.wrong_card_info)
    
    def test_invalid_operation(self):
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.enter_pin(self.wrong_card_info)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.select_account()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.see_balance()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.deposit(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.withdraw(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.cancel()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.eject_card()

class TestCardInsertState(unittest.TestCase):
    def setUp(self):
        self.card_info = {'card_number':'1234-5678-1234-5678','pin':'1234'}
        card = Card(self.card_info)
        self.state = State.CardInsertedState(card)
        
    def test_enter_pin_correct(self):
        next_state = self.state.enter_pin('1234')
        self.assertIsInstance(next_state, State.SelectAccountState)

    def test_enter_pin_incorrect(self):
        with self.assertRaises(Exceptions.InvalidValueError):
            next_state = self.state.enter_pin('0000')
    
    def test_cancel(self):
        next_state = self.state.cancel()
        self.assertIsInstance(next_state, State.EjectCardState)

    def test_invalid_operation(self):
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.insert_card(self.card_info)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.select_account()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.see_balance()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.deposit(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.withdraw(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.eject_card()

class TestSelectAccountState(unittest.TestCase):
    def setUp(self):
        self.card_info = {'card_number':'1234-5678-1234-5678','pin':'1234'}
        self.card = Card(self.card_info)
        self.state = State.SelectAccountState(card=self.card)
        
    def test_select_account(self):
        next_state = self.state.select_account()
        self.assertIsInstance(next_state, State.TransactionState)
    
    def test_cancel(self):
        next_state = self.state.cancel()
        self.assertIsInstance(next_state, State.EjectCardState)

    def test_invalid_operation(self):
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.insert_card(self.card_info)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.enter_pin("1234")
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.see_balance()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.deposit(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.withdraw(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.eject_card()

class TestTransactionState(unittest.TestCase):
    def setUp(self):
        self.account = Account(card_num='1234-5678-1234-5678',balance=100)
        self.state = State.TransactionState(self.account)
    
    def test_get_balance(self):
        self.state.see_balance()
        initial_balance = 100
        self.assertEqual(initial_balance, self.state.cur_balance)
    
    def test_deposit(self):
        self.state.deposit(10)
        initial_balance = 100
        self.assertEqual(initial_balance+10, self.state.selected_account.balance)

    def test_withdraw_sufficient_balance(self):
        self.state.withdraw(10)
        initial_balance = 100
        self.assertEqual(initial_balance-10, self.state.selected_account.balance)

    def test_withdraw_insufficient_balance(self):
        #initial_balance = 100
        with self.assertRaises(Exceptions.InsufficientBalanceError):
            self.state.withdraw(200)

    def test_cancel(self):
        next_state = self.state.cancel()
        self.assertIsInstance(next_state, State.EjectCardState)


    def test_invalid_operation(self):
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.insert_card(dict())
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.enter_pin("1234")
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.select_account()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.eject_card()

class TestEjectCardState(unittest.TestCase):
    def setUp(self):
        self.state = State.EjectCardState()
    
    def test_eject_card(self):
        next_state = self.state.eject_card()
        self.assertIsInstance(next_state, State.IdleState)

    def test_invalid_operation(self):
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.insert_card(dict())
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.enter_pin("1234")
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.select_account()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.see_balance()
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.deposit(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.withdraw(10)
        with self.assertRaises(Exceptions.InvalidOperationError):
            next_state = self.state.cancel()

