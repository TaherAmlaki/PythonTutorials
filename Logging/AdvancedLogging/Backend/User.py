from Backend import logger


class User:
    def __init__(self, name, account):
        self.name = name 
        self.account = account  # an Account instance

        logger.info(f"Created A new User: {self}")

    def __repr__(self):
        return f"User(name={self.name}, account={self.account})"
