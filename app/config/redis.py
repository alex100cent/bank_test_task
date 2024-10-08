from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379
    password: str = "redis_pass_1234"

    class Config:
        env_prefix = "redis_"
        env_file = ".env"
