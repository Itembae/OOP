from account import Account, CheckingsAccount, SavingsAccount
from transaction import Transaction
from comparable import ComparableMixin


class Bank:
    def __init__(self):
        self._accounts = []
    
    def new_account(self, account_type):
        """Creates a new account of type checking or savings, depending on user input
        """
        if account_type == "checking":
            n = CheckingsAccount()
        elif account_type == "savings":
            n = SavingsAccount()
        self._accounts.append(n)
        return n
    
    def all_accounts(self):
        """used to access the list of all accounts for "summary"""
        return self._accounts
    
    def select(self, id):
        """compares user given id to every account number and returns the matching account
        """
        accounts = self.all_accounts()
        for account in accounts: 
            number = getattr(account, '_id')
            if int(number) == int(id):
                return account
