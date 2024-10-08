import json
from redis import Redis

from app.config import redis as redis_config, application


class CacheService:
    def __init__(self):
        self.redis = Redis(
            host=redis_config.host,
            port=redis_config.port,
            password=redis_config.password,
        )

    def set_cache(self, key: str, value, ttl: int = 5) -> None:
        ttl = ttl or application.redis_ttl
        self.redis.set(key, json.dumps(value), ex=ttl)

    def get_cache(self, key: str):
        json_data = self.redis.get(key)
        if json_data:
            return json.loads(json_data)
        return None


cache_service = CacheService()
