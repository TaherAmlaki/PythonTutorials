from datetime import datetime
from ShoppingListApp.DB.postgresql import db
from ShoppingListApp.DB.base_model import BaseModel


ItemShop = db.Table(
    'ItemShop',
    db.Column('shoppinglist_id', db.Integer, db.ForeignKey('shoppinglist.id')),
    db.Column('item_id', db.Integer),
    db.Column('item_name', db.String),
    db.ForeignKeyConstraint(['item_id', 'item_name'], ['item.id', 'item.name']),
    db.UniqueConstraint('shoppinglist_id', 'item_name')
)


class ShoppingListModel(BaseModel):
    __tablename__ = "shoppinglist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(15), default="created")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    items = db.relationship('ItemModel',
                            secondary=ItemShop,
                            lazy='subquery',
                            backref=db.backref("shoppinglist", lazy=True))

    @classmethod
    def get_paginator(cls, user_id, page_number):
        return cls.query.filter_by(user_id=user_id).paginate(page=page_number, per_page=5)

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


class ItemModel(BaseModel):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    price = db.Column(db.Float(precision=2), nullable=True)

