import logging

logging.basicConfig(filename="../person.log",
                    filemode="w",
                    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
                    level=logging.INFO)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        logging.info(f"New Person instance is created => {self}")

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"


# me = Person("Taher", 30)
