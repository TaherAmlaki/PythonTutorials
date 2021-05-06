from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from app.db.postgresql import Base, session


ShoppingItem = Table(
    "shopping_item",
    Base.metadata,
    Column("shoppinglist_id", ForeignKey("shoppinglist.id"), primary_key=True),
    Column("item_id", ForeignKey("item.id"), primary_key=True)
)


class ItemModel(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"ItemModel(id={self.id}, name={self.name})"


class ShoppingListModel(Base):
    __tablename__ = "shoppinglist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    status = Column(String(20))
    items = relationship("ItemModel", secondary=ShoppingItem,
                         backref=backref("shoppinglists"))

    @classmethod
    def find_all_by_user_id(cls, user_id) -> List["ShoppingListModel"]:
        return session.query(cls).filter_by(user_id=user_id).all()

    def save_to_db(self) -> None:
        session.add(self)
        session.commit()

    def delete_from_db(self) -> None:
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"ShoppingListModel(id={self.id}, user_id={self.user_id}, " \
               f"status={self.status}, items={self.items})"
