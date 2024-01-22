import redis


class CacheApp:
    def __init__(self, nodes):
        self.nodes = nodes
        self.connections = [redis.StrictRedis(host='localhost', port=node, decode_responses=True) for node in nodes]

    def _get_connection(self, key):

        node_index = hash(key) % 3

        return self.connections[node_index]

    def put(self, key, value):
        connection = self._get_connection(key)
        connection.set(key, value)

    def get(self, key):
        connection = self._get_connection(key)
        return connection.get(key)

    def delete(self, key):
        connection = self._get_connection(key)
        connection.delete(key)

if __name__ == "__main__":
    nodes = [7000, 7001, 7002]

    cache_app = CacheApp(nodes)

    cache_app.put(1, "Anjali")

    result_before_delete = cache_app.get(1)
    print("Get result for key:", result_before_delete)

    cache_app.delete(1)

    result_after_delete = cache_app.get(1)
    print("Get result for name after deletion:", result_after_delete)