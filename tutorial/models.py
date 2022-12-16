import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    fullname = sa.Column(sa.String(50))

    def __repr__(self) -> str:
        return f'<User(name={self.name!r}, fullname={self.fullname!r})>'
