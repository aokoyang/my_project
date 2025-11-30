import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def add_token_to_blacklist(token: str, expire: int):
    """将 access token 加入黑名单，有效期 = 原本剩余时间"""
    redis_client.setex(f"blacklist:{token}", expire, "true")

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") > 0