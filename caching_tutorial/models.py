import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    is_active = sa.Column(sa.Boolean, default=True)

    addresses = orm.relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id!r} name={self.name!r}, is_active={self.is_active!r})>"
        )


class Address(Base):
    __tablename__ = "addresses"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(50))
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    user = orm.relationship(User, back_populates="addresses")

    def __repr__(self) -> str:
        return f"<Address(id={self.id!r} email={self.email!r})>"
