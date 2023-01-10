import pickle

import sqlalchemy as sa
from sqlalchemy.orm.session import make_transient_to_detached

from caching_tutorial.models import User
from caching_tutorial.query import CachingQuery


def test_query_instance_is_caching_query(session):
    query = session.query(User)

    assert isinstance(query, CachingQuery)


def test_db_instance_state_after_pickling(session):
    session.add(User(id=1, name="John Wick"))
    # session.commit()

    user = session.query(User).one()

    assert sa.inspect(user).persistent

    raw_data = pickle.dumps(user)
    cached_user = pickle.loads(raw_data)

    assert sa.inspect(cached_user).detached


def test_query_results_from_cache(session):
    query = session.query(User)

    cached_user = User(id=1, name="John Wick")
    make_transient_to_detached(cached_user)
    cache_key = query.cache_key()
    query.cache[cache_key] = pickle.dumps([cached_user])

    user = query.one()

    assert user.id == 1
    assert user.name == "John Wick"
    assert len(user.addresses) == 0


def test_query_results_into_and_from_cache(session):
    # Let's populate the database with some data
    user = User(id=1, name="John Wick")
    session.add(user)
    session.commit()

    query = session.query(User)
    cache_key = query.cache_key()

    # The cache is empty
    assert cache_key not in query.cache

    user = query.one()

    # The cache is filled with the query results
    assert cache_key in query.cache

    # Let's validate that the query don't hit the database
    # if the cache is filled
    query.error_on_cache_miss = True
    user = query.one()

    assert user.id == 1
    assert user.name == "John Wick"
    assert len(user.addresses) == 0
