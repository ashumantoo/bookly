from redis import asyncio as aioredis
from src.config import Config
from src.constants import JTI_EXPIRY

redis_client = aioredis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True,
)


async def add_jti_to_blocklist(email: str, jti: str) -> None:
    # TTL is hardcode to 1hr but it should be calculated according to the reming expiration time of access_token
    await redis_client.set(name=f"{email}:{jti}", value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await redis_client.get("jti")
    return jti is not None
