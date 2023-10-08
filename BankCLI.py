import sys
import pickle
from bank import Bank
from transaction import Transaction
from exception import TransactionSequenceError, OverdrawError, TransactionLimitError
import decimal
from decimal import Decimal
import datetime
import logging

# '%(asctime)s |%(levelname)-4s| %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logging.basicConfig(filename='bank.log', level=logging.DEBUG, format="")
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
        while True:
            try:
                t = Transaction(deposit)
                break
            except decimal.InvalidOperation:
                print("Please try again with a valid dollar amount.")
                deposit = input("Initial deposit amount?\n>")
            
        n = self._bank.new_account(account_type)
        n.new_transaction(t)
        logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Created account: {}".format(n._id))
        
        
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
        try:
            ledger = self._selected_account.ordered_transactions()
            for item in ledger: 
                print(item)
        except AttributeError:
            print("This command requires that you first select an account.")
      
            
    def _add_transaction(self):
        """create a transaction and add it to the selected account if valid
        """  
        amount = input("Amount?\n>")
        while True:
            try: 
                Decimal(str(amount))
            except decimal.InvalidOperation:
                print("Please try again with a valid dollar amount.")
                amount = input("Amount?\n>")
            break
        date = input("Date? (YYYY-MM-DD)\n>")
        # had to separate the while loops to keep from double prompting for amount
        while True:
            try:
                new = Transaction(amount, date)
                break
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD.")
                date = input("Date? (YYYY-MM-DD)\n>")
            
        
        # check actual account transaction errors
        try:
            self._selected_account.new_transaction(new)
        except AttributeError:
            print("This command requires that you first select an account.")
        except OverdrawError:
            print("This transaction could not be completed due to an insufficient account balance.")
        except TransactionLimitError as e:
            print("This transaction could not be completed because this account already has {} transactions in this {}.".format(e.limit_violated, e.time))
        except TransactionSequenceError as e:
            print("New transactions must be from {} onward.".format(e.oldest_date))
        
        
    def _interest_fees(self):
        """calls function to check account interest rates and balance threshold, and updates balance accordingly
        """
        try:
            self._selected_account._check_fees()
            logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Triggered fees and interest")
        except AttributeError:
            print("This command requires that you first select an account.")
        except TransactionSequenceError as e:
            print("Cannot apply interest and fees again in the month of {}.".format(e.oldest_date.strftime("%B")))
            
    def _save(self):
        """_summary_
        """
        with open("bank.pickle", "wb") as f:
            pickle.dump(self._bank, f)
            logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Saved to bank.pickle")
            
    def _load(self):
        with open("bank.pickle", "rb") as f:   
            self._bank = pickle.load(f)
            logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|DEBUG|' + "Loaded from bank.pickle")
            
    def _quit(self):
        sys.exit(0)
        
if __name__ == "__main__":
    try:
        BankCLI().run()
    except Exception as e:
        print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
        logging.debug(f'{datetime.datetime.now().replace(microsecond = 0)}|ERROR|{type(e).__name__}:' + f"{repr(str(e))}")
        exit(0)

