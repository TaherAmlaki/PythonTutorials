from Backend import logger


class Account:
    def __init__(self, account_type, account_number):
        self.account_type = account_type 
        self.account_number = account_number 

        logger.info(f"Created A new Account: {self}")

    def __repr__(self):
        return f"Account(account_type={self.account_type}, account_number={self.account_number})"
