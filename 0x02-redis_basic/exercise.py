#!/usr/bin/env python3
"""module to create a cache class"""


import redis
import uuid

class Cache:
    """a simple caching class"""
    _redis = ''
    def __init__(self):
        """special method to initialize the attributes"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """method to store data in redis.
        data(bytes): value to be assigned to a random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
