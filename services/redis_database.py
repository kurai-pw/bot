import redis


class Redis:

    @staticmethod
    def conn():
        return redis.Redis()

    @staticmethod
    def set(key, value, **kwargs):
        return Redis.conn()\
            .set(key, value, **kwargs)

    @staticmethod
    def get(key):
        value = Redis.conn()\
            .get(key)
        if value:
            return value
        return None
