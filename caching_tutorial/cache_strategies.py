import pickle


class CacheMissError(Exception):
    """Raised when the cache miss occurs."""


class InMemoryCacheStrategy:
    def __init__(self):
        self.cache = {}
        self.error_on_cache_miss = False

    def exec(self, query):
        cache_key = self.cache_key(query)
        raw_data = self.cache.get(cache_key)

        if raw_data is None:
            if self.error_on_cache_miss:
                raise CacheMissError("Cache miss for key: {}".format(cache_key))
            result = list(query.__iter__())
            self.cache[cache_key] = pickle.dumps(result)
        else:
            result = pickle.loads(raw_data)

        return query.merge_result(result, load=False)

    def cache_key(self, query):
        "Use the query's SQL statement and parameters as the cache key"
        stmt = query.with_labels().statement
        compiled = stmt.compile()
        params = compiled.params
        cache_key = " ".join([str(compiled)] + [str(params[k]) for k in sorted(params)])

        return cache_key


class CacheStoreStrategy:
    def __init__(self, cache, cache_key):
        self.cache = cache
        self.error_on_cache_miss = False
        self._cache_key = cache_key

    def exec(self, query):
        cache_key = self.cache_key(query)
        raw_data = self.cache.get(cache_key)

        if raw_data is None:
            if self.error_on_cache_miss:
                raise CacheMissError("Cache miss for key: {}".format(cache_key))
            result = list(query.__iter__())
            self.cache[cache_key] = pickle.dumps(result)
        else:
            result = pickle.loads(raw_data)

        return query.merge_result(result, load=False)

    def cache_key(self, query):
        return self._cache_key
