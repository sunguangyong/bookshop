# -*- coding: utf-8 -*- 

import redis



def redis_conn(host="localhost", port=6379, decode_responses=True):
    pool = redis.ConnectionPool(host=host, port=port, decode_responses=decode_responses)
    r = redis.Redis(connection_pool=pool)
    return r


if __name__ == '__main__':
    client  = redis_conn("172.16.15.245") 

    client.sadd("fb", "23")
    client.sadd("fb", "23")
    client.sadd("fb", "abcd")
    client.sadd("fb", "ssssssss")


    print list(client.smembers("fb"))
    print list(client.smembers("fb2"))

    client.hset("a", "1", "one")
    client.hset("a", "2", "tow")


    print client.hgetall("a")
