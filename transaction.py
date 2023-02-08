import datetime
from decimal import Decimal, setcontext, BasicContext
from comparable import ComparableMixin

setcontext(BasicContext)

class Transaction():
    # date, amount; deposit or withdrawals
    def __init__(self, amount = 0, date = None, status = False):
        if date is None: 
            self._date = datetime.date.today()
        else: 
            self._date = self._date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self._status = status
        self._amount = Decimal(str(amount))
        
    def _get_time(self):
        """ used to access transaction date externally"""
        return self._date
    
    def get_status(self):
        """used for external access to transaction status as exempt from limits"""
        return self._status
        
    def __lt__(self, compared):
        """allows date comparison for sorting"""
        return self._date < compared._date
    
    def __str__(self):
        """date and time formatting""" 
        return f'{self._date}' + ", " + "${:,.2f}".format(self._amount)
        
    def _check_month(self, second):
        "check if two transactions share the same month"
        return self._date.month == second._date.month and self._date.year == second._date.year
