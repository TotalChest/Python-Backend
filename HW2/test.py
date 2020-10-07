from cache import LRUCache

cache = LRUCache(1)
cache.set('Jesse', 'Pinkman')
cache.set('Walter', 'White')
cache.set('Jesse', 'James')
print(cache.get('Jesse'))
cache.delete('Walter')
print(cache.get('Walter'))