from sqlalchemy.orm import sessionmaker

from .query import CachingQuery

Session = sessionmaker(query_cls=CachingQuery)
