import json
from typing import Any

import redis.asyncio as redis



REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0

# 创建redis客户端(Redis的连接对象)
redis_client = redis.Redis(
    host=REDIS_HOST,# redis主机
    port=REDIS_PORT,# redis端口
    db=REDIS_DB,# redis数据库索引
    decode_responses=True,# 是否将响应值解码为字符串
)
#读取字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None
#读取json字符串
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)# 解析json字符串
        return None
    except Exception as e:
        print(f"获取json缓存失败: {e}")
        return None

#设置字符串缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)# 设置缓存过期时间
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
