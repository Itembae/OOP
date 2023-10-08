class OverdrawError(Exception):
    pass

class TransactionSequenceError(Exception):
    def __init__(self, date):
           super().__init__(date)
           self.oldest_date = date
           
class TransactionLimitError(Exception):
    def __init__(self, limit, period):
           super().__init__(limit)
           self.limit_violated = limit
           self.time = period
