from sqlalchemy.orm.interfaces import MapperOption


class with_caching_strategy(MapperOption):
    def __init__(self, strategy):
        self.strategy = strategy

    def process_query(self, query):
        query.caching_strategy = self.strategy
