from typing import List

from . import postgredb as db


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_name(cls, name: str) -> __qualname__:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_: str) -> __qualname__:
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls) -> List[__qualname__]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
