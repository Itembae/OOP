import sys
import pickle
from bank import Bank
from transaction import Transaction
from account import Account

class BankCLI:
    """Display a menu and respond to choices when run."""
    def __init__(self):
        self._bank = Bank()
        self._selected_account = None
        
        self._choices = {
            "1": self._open_account,
            "2": self._summary,
            "3": self._select_account,
            "4": self._list_transactions,
            "5": self._add_transaction,
            "6": self._interest_fees,
            "7": self._save,
            "8": self._load,
            "9": self._quit,
        }
    
    def _display_menu(self):
        print(f"""--------------------------------
Currently selected account: {self._selected_account}
Enter command
1: open account
2: summary
3: select account
4: list transactions
5: add transaction
6: interest and fees
7: save
8: load
9: quit""")

    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def _open_account(self):
        """Take user input and create the specified account
        """
        account_type = input("Type of account? (checking/savings)\n>")
        deposit = input("Initial deposit amount?\n>")
        t = Transaction(deposit)
        n = self._bank.new_account(account_type)
        n.new_transaction(t)
        
        
    def _summary(self):
        """List every account created and its balance
        """
        accounts = self._bank.all_accounts()
        for account in accounts:

            print(account)
            

    def _select_account(self):
        """search and select the account matching user specified account number """
        id = input("Enter account number\n>")
        selected = self._bank.select(id)
        self._selected_account = selected
        
    def _list_transactions(self):
        """list all transactions for the selected account
        """
        ledger = self._selected_account.ordered_transactions()
        for item in ledger: 
            print(item)
            
    def _add_transaction(self):
        """create a transaction and add it to the selected account if valid
        """
        amount = input("Amount?\n>")
        date = input("Date? (YYYY-MM-DD)\n>")
        new = Transaction(amount, date)
        self._selected_account.new_transaction(new)
        
        
    def _interest_fees(self):
        """calls function to check account interest rates and balance threshold, and updates balance accordingly
        """
        self._selected_account._check_fees()
        
    def _save(self):
        """_summary_
        """
        with open("bank_save.pickle", "wb") as f:
            pickle.dump(self._bank, f)
            
    def _load(self):
        with open("bank_save.pickle", "rb") as f:   
            self._bank = pickle.load(f)
            
    def _quit(self):
        sys.exit(0)
        
if __name__ == "__main__":
    BankCLI().run()

