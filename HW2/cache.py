"""LRU algorithm"""


class LRUCache:
    """LRU algorithm"""
    def __init__(self, capacity: int=10) -> None:
        self.capacity = capacity
        self.time = 0
        self.cache = {}
        self.timing = {}

    def get(self, key: str) -> str:
        """Return value by key. If not exist return '' """
        self.time += 1
        self.timing[key] = self.time
        return self.cache.get(key, '')

    def set(self, key: str, value: str) -> None:
        """Set or update value by key"""
        self.time += 1
        if len(self.cache) < self.capacity:
            self.cache[key] = value
            self.timing[key] = self.time
        else:
            if key in self.cache:
                self.cache[key] = value
                self.timing[key] = self.time
            else:
                min_time = min(self.timing.values())
                keys = list(self.timing.keys())
                del_key = keys[list(self.timing.values()).index(min_time)]
                self.cache.pop(del_key)
                self.timing.pop(del_key)
                self.cache[key] = value
                self.timing[key] = self.time

    def delete(self, key: str) -> None:
        """Delete element from dict if it exist"""
        self.cache.pop(key, None)
        self.timing.pop(key, None)
