import pickle

from sqlalchemy import orm


class CacheMissError(Exception):
    """Raised when the cache miss occurs."""


class CachingQuery(orm.Query):
    def __init__(self, *args, cache=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache or {}
        self.error_on_cache_miss = False

    def __iter__(self):
        cache_key = self.cache_key()
        raw_data = self.cache.get(cache_key)

        if raw_data is None:
            if self.error_on_cache_miss:
                raise CacheMissError("Cache miss for key: {}".format(cache_key))
            result = list(super().__iter__())
            self.cache[cache_key] = pickle.dumps(result)
        else:
            result = pickle.loads(raw_data)

        return self.merge_result(result, load=False)

    def cache_key(self):
        "Use the query's SQL statement and parameters as the cache key"
        stmt = self.with_labels().statement
        compiled = stmt.compile()
        params = compiled.params
        cache_key = " ".join([str(compiled)] + [str(params[k]) for k in sorted(params)])

        return cache_key
