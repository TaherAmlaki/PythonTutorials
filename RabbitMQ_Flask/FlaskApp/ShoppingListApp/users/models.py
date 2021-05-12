import bcrypt
from flask_login import UserMixin

from ShoppingListApp.db import postgredb as db
from ShoppingListApp.db import BaseModel

from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(user_id)


class UserModel(BaseModel, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, unique=True)

    shopping_lists = db.relationship('ShoppingListModel',
                                     backref=db.backref("user", lazy='select'),
                                     lazy='select',
                                     cascade="all, delete, delete-orphan")

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def is_password_match(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"User(username={self.username}, id={self.id})"

