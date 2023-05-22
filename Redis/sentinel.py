"""Redis connection test using Sentinel"""

import redis
from redis import Sentinel


def get_redis(nodes: list) -> redis.Redis:
    """Function which return master"""
    sentinel = Sentinel(nodes)

    # Show master
    print(f"Redis master instance -> {sentinel.discover_master('mymaster')}")
    # Show slaves
    print(f"Redis slave instances -> {sentinel.discover_slaves('mymaster')}")

    host, port = sentinel.discover_master("mymaster")
    connection = redis.StrictRedis(host=host, port=port, password="pass")
    print(connection.ping())

    return connection


if __name__ == "__main__":

    r = get_redis(
        [("192.168.55.21", 5000), ("192.168.55.22", 5000), ("192.168.55.23", 5000)]
    )

    print(r.ping())
    print(r.exists("4"))
    print(r.set("4", "d"))
