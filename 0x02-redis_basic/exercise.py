#!/usr/bin/env python3
"""module to create a cache class"""


from typing import Callable, Optional, Union, Any
import redis
import uuid

class Cache:
    """a simple caching class"""
    _redis = ''
    def __init__(self):
        """special method to initialize the attributes"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method to store data in redis.
        data(bytes): value to be assigned to a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value
    def get_str(key: str) -> str:
        return str(self._redis.get(key))
    def get_int(key: str) -> int:
        return int(self._redis.get(key))
