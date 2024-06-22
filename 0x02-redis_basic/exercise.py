#!/usr/bin/env python3
"""module to create a cache class"""


from typing import Callable, Optional, Union, Any
import redis
import uuid
from functools import wraps

def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper

class Cache:
    """a simple caching class"""
    def __init__(self):
        """special method to initialize the attributes"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
