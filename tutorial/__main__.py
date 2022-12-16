from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)

models.Base.metadata.create_all(engine)

session = Session()

session.add(models.User(name='ed', fullname='Ed Jones'))
session.commit()

for user in session.query(models.User):
    print(user)
