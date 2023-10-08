from decimal import Decimal, setcontext, BasicContext
from transaction import Transaction
from exception import OverdrawError, TransactionLimitError, TransactionSequenceError
import datetime
from datetime import timedelta
import logging

class Account():
    # Store the next available id for all new notes
    last_id = 0
    oldest_date = datetime.date.today()
    fees = False
    def __init__(self):
        Account.last_id += 1
        self._id = Account.last_id
        self._transactions = []
        self._oldest = Account.oldest_date
        self._fees = Account.fees
        
    def new_transaction(self, transaction):
        """takes an incoming transaction and checks to see if it is valid before processing it to an account
        """
        # check to make sure transaction does not over draw the account
        overdrawn = self._check_balance(transaction)
        # check whether the daily/monthly limits have been reached
        limited = self._check_limits(transaction) 
        if overdrawn and limited:
            if transaction._date < self._oldest:
                raise TransactionSequenceError(self._oldest)
            else:
                self._transactions.append(transaction)
                self._fees = False
                #updates the last used date
                self._oldest = transaction._date
                # maybe do this in create account and add transaction separately
                logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Created transaction: {}, {}".format(self._id, transaction._amount))
        else:
            if overdrawn == False:
                raise OverdrawError
            
            
    def _check_limits(self, transaction):
        return True     
    
    def _check_balance(self, transaction):
        """returns false if an incoming transaction will overdraw the account, true if it is fine
        """
        ta = getattr(transaction, '_amount')
        return ( int(ta) + int(self.current_balance()) >= 0)
        
    def current_balance(self):
        """tracks all transactions associated with an account to return the current balance"""
        sum = 0
        for item in self._transactions:
            amount = getattr(item, '_amount')
            sum += amount
        return sum
    
    def _check_fees(self):
        """calculate the fees associated with an account and processes that transaction
        """
        balance = self.current_balance()
        interest = self._interest_rate * balance
        if self._fees == True:
            raise TransactionSequenceError(self._oldest)
        else:
            latest = self._oldest
            next_month = latest.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            n = Transaction(interest, str(last_day), status = True)
            logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Created transaction: {}, {}".format(self._id, interest))
            # add that transaction to the account list
            self._fees = True
            self._transactions.append(n)
            self._oldest = last_day
        
    def ordered_transactions(self):
        """arranges a transaction list by date and returns the ordered list
        """
        return sorted(self._transactions)
    
    def __str__(self):
        """formatting for the printing of account information "Account Number, Balance: "
        """
        return f"#{self._id:09},\tbalance: ${self.current_balance():,.2f}"
       
class SavingsAccount(Account):
    def __init__(self):
        super().__init__()
        self._type = "Savings"
        self._interest_rate = Decimal("0.029")
        self._daily_limit = 2
        self._monthly_limit = 5
        
    def _check_limits(self, transaction):
        """add up the transactions associated with an account
        """
        daily = 0
        monthly = 0
        for date in self._transactions:
            if date.get_status() != True:
                if transaction._date == date._date:
                    daily += 1
                if transaction._check_month(date):
                    monthly += 1  
        if daily >= self._daily_limit:
            raise TransactionLimitError(self._daily_limit, "day")
        if monthly >= self._monthly_limit:
            raise TransactionLimitError(self._monthly_limit, "month")
        
        return daily < self._daily_limit and monthly < self._monthly_limit
    
    def __str__(self):
        return "Savings" + super().__str__()
        
        
class CheckingsAccount(Account):
    def __init__(self):
        super().__init__()
        self._type = "Checking"
        self._interest_rate = Decimal("0.0012")
        self._balance_threshold = 100
        self._low_balance_fee = -10
        
    def _check_fees(self):
        """checks account balance agaisnt minimum required balance and processes fee if lower
        """
        super()._check_fees()

        balance = self.current_balance()
        if balance < self._balance_threshold:
            latest = self._oldest
            next_month = latest.replace(day=28) + timedelta(days=4)
            last_day = next_month - timedelta(days=next_month.day)
            fee = Transaction(self._low_balance_fee, str(last_day), status = True)
            # transaction log for fees
            logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Created transaction: {}, {}".format(self._id, self._low_balance_fee))
            self._transactions.append(fee)
            self._oldest = last_day
            
    def __str__(self):
        """Formats the type, account number, and balance of the account.
        For example, 'Checking#000000001,<tab>balance: $50.00'
        """ 
        return "Checking" + super().__str__()
            
            
