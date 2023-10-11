import redis 
from config.config import REDIS_DB, REDIS_HOST, REDIS_PORT

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
