#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import redis
import ConfigParser
#from multi_log import init_log,debug_log,info_log,error_log

RETRY_TIMEOUT_FACTOR = 5
RECONNECT_TIME = 30*2000000
#RECONNECT_TIME = 60*3

#redis命令重试次数(0、1,共两次)
RETRY_REDIS_COMMAND_EXECUTE_TIMES = 1

####################
#封装redis库
#####################
class redis_cache():
    def __init__(self, config_path=None, config_dic=None):
        self.redis_inst = None
        self.pool = None
        self.init(config_path=config_path, config_dic=config_dic)

    def print_server(self):
        raise NotImplementedError()

    def init(self, config_path=None, config_dic=None):
        try:
            print config_path
            if config_path is None and config_dic is None:
                config_dic = {}
                #raise ValueError("config_path and config_dic is None") 
            if config_path is not None:
            	config_parser = ConfigParser.SafeConfigParser({
                    'host':'127.0.0.1',
                    'port':6379,
                    'db':0,
                    'max_conn':5,
                    'timeout':10
                })
                config_parser.read(config_path)
                my_host = config_parser.get('REDIS', 'host')
                my_port = config_parser.getint('REDIS', 'port')
                my_db = config_parser.getint('REDIS', 'db')
                my_max_conn = config_parser.getint('REDIS', 'max_conn')
                my_timeout = config_parser.getint('REDIS', 'timeout')
            else:
                my_host = config_dic.get('host') or '127.0.0.1'
                my_port = config_dic.get('port') or 6379
                my_db = config_dic.get('db') or 0
                my_max_conn = config_dic.get('max_conn') or 5
                my_timeout = config_dic.get('timeout') or 10
            
            self.pool = redis.ConnectionPool(host=my_host, port=my_port, db=my_db, max_connections=my_max_conn)
            self.redis_inst = redis.Redis(connection_pool=self.pool,socket_timeout=my_timeout)
            self.redis_inst.ping()
            
            print "Redis Connect,host=%s,port=%d,db=%d" % (my_host,my_port,my_db)
        except Exception, error:
            raise ValueError("redis init failed, error=%s" % str(error))
    #
    #获取redis_server的基础配置信息
    #
    def __init_redis_server_config(self,cfgparser,section,server,read):
        raise NotImplementedError()
    def __allconnect(self):
        raise NotImplementedError()
    def __release_server(self,server):
        raise NotImplementedError()
    def __ping_server(self,server):
        raise NotImplementedError()
    def __connect_server(self,server):
        raise NotImplementedError()
    def __auth_server(self,server):
        raise NotImplementedError()
    #
    # 尝试恢复所有down掉的服务器
    #
    def __up_servers(self):
        raise NotImplementedError()
    #
    # 选择一个可用的读服务器
    # 每次选择后都要查看是否有down服务器,有则需要增加_reader_use_times次数,
    # 并且每隔retry_connect_times重试次数之后尝试恢复所有down服务器
    # 目的：尽量保证随时有可用服务器,进行可读服务器的重连机制
    #
    def __select_reader(self):
        raise NotImplementedError()
    #
    #挂掉某个服务器:仅将broken字段设为True,redis上下文不置空
    #
    def __down_server(self,server):
        raise NotImplementedError()
    #
    # 重连激活rediscontext
    #
    def active_server(self):
        raise NotImplementedError()
    #
    # 获取服务器
    #
    def __get_server(self,write):
        raise NotImplementedError()

    """
    # function：获取redis_server连接句柄[即可操作任何redis命令的连接句柄]
    # return：  失败抛出异常，成功返回连接句柄
    """
    def get_redis_server(self,write):
        raise NotImplementedError()

    """
    # function：redis命令执行工厂函数，至多执行两次命令
    # return：  根据redis命令返回
    """
    def __redisCommand(self,server,command_name,*args,**kwargs):
        raise NotImplementedError()

    def get_inst(self):
        return self.redis_inst

    """
    # function：将内容以strings格式存到cache，且内容不会过期[set]
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def put_to_cache(self,key,val):
        if key is None or val is None:
            raise ValueError("params invalid")
        #debug_log("Redis put_to_cache, key=%s, val=%s", key, str(val))
        self.redis_inst.set(key,val)

    """
    # function：批量将内容以strings格式存到cache，且内容不会过期[set]
    # args:     key_value字典
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    #------新添加------
    def put_multi_to_cache(self,**args):
        if args is None:
            raise ValueError("args invalid")
        #debug_log("Redis put_multi_to_cache, args=%s", str(args))
        self.redis_inst.mset(args)

    """
    # function：将内容以strings格式存到cache，且设置内容过期时间[setex]
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def put_to_cache_ex(self,key,val,timeout):
        if key is None or val is None or timeout is None:
            raise ValueError("params invalid")
        assert timeout > 0, "timeout must > 0"
        #debug_log("Redis put_to_cache_ex, key=%s, val=%s, timeout=%d", key, str(val), timeout)
        self.redis_inst.setex(key,val,timeout)

    """
    # function：获取strings格式存储在cache的内容[get]
    # return：  失败抛出异常，成功返回str内容(key不存在返回None)
    """
    def get_from_cache(self,key):
        if key is None:
            raise ValueError("params invalid")
        res = self.redis_inst.get(key)
        #debug_log("Redis get_from_cache, key=%s, res=%s", key, str(res))
        return res

    """
    # function：获取strings格式存储在cache的内容[mget]
    # return：  失败抛出异常，成功返回[v1,v2](key不存在对应位置返回None)
    """
    def get_multi_from_cache(self,*key):
        if key is None or not key:
            raise ValueError("params invalid")
        res = self.redis_inst.mget(*key)
        #debug_log("Redis get_multi_from_cache, key=%s, res=%s", key, str(res))
        return res

    """
    # function：删除cache内容，可批量删除keys[delete]
    # return：  失败抛出异常，成功正常删除且无异常抛出
    """
    def del_from_cache(self,*key):
        if key is None or not key:
            raise ValueError("params invalid")
        #debug_log("Redis del_from_cache, key=%s", key)
        return self.redis_inst.delete(*key)

    """
    # function：自增key[incr]
    # return：  失败抛出异常，成功返回自增的int结果值
    """
    def incr_key(self,key):
        if key is None:
            raise ValueError("params invalid")
        return self.redis_inst.incr(key)

    """
    # function：设置key过期[expire]
    # return：  失败抛出异常，成功正常设置过期时间且无异常抛出
    """
    def set_key_expire(self,key,timeout):
        if key is None or timeout is None:
            raise ValueError("params invalid")
        #debug_log("Redis set_key_expire, key=%s, timeout=%d", key, timeout)
        return self.redis_inst.expire(key, timeout)

    """
    # function：将内容以sorted set结构存到cache[zadd]
    # args:     val和score一对,valist和sclist一对，必须成对同时出现
    #            valist:[v1,v2], sclist:[score1,score2]
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def add_to_sorted_set(self,key,val=None,score=None,valist=None,sclist=None,vslist=None):
        #debug_log("Redis add_to_sorted_set, key=%s,val=%s,score=%s,valist=%s,sclist=%s,vslist=%s",\
        #                        key,str(val),str(score),str(valist),str(sclist),str(vslist))
        if key is None:
            raise ValueError("key invalid")
        val_arr = []
        if val is not None and score is not None:
            val_arr.append(val)
            val_arr.append(score)
            return self.redis_inst.zadd(key,*val_arr)
        if valist is not None and sclist is not None:
            for i in range(len(valist)):
                val_arr.append(valist[i])
                val_arr.append(sclist[i])
            return self.redis_inst.zadd(key,*val_arr)
        if vslist is not None:
            return self.redis_inst.zadd(key,*vslist)
        raise ValueError("params invalid")

    """
    # function：计算sorted set结构的元素总数[zcard]
    # return：  失败抛出异常，成功返回元素总数
    """
    def get_num_from_sorted_set(self,key):
        if key is None:
            raise ValueError("key invalid")
        res = self.redis_inst.zcard(key)
        #debug_log("Redis get_num_from_sorted_set, key=%s, res=%s", key, str(res))
        return res

    """
    # function：根据score计算sorted set结构的元素总数[zcount]
    # args:     闭合区间可选，startid:起始score(不包含startid传'(startid')，endid:结束score(不包含endid传'(endid')')')')')
    # return：  失败抛出异常，成功返回元素总数
    """
    #------新添加------
    def get_num_from_sorted_set_by_score(self,key,startid,endid):
        if key is None or startid is None or endid is None:
            raise ValueError("params invalid")
        return self.redis_inst.zcount(key,startid,endid)

    """
    # function：获取sorted set结构的内容[zrange]
    # args:     start偏移位，count获取总数，皆不能小于0
    #           reverse默认按score倒序返回
    #           count=0默认取整个有续集成员
    # return：  失败抛出异常，成功返回列表结构:[('v1',score1),('v2',score2)]
    """
    #------修改------
    def get_from_sorted_set(self,key,start=0,count=0,reverse=True,score=True):
        #debug_log("Redis get_from_sorted_set, key=%s, start=%d, count=%d, reverse=%s, score=%s",\
        #                        key, start, count, str(reverse), str(score))
        if key is None:
            raise ValueError("params invalid")
        assert start>=0 and count>=0, "start and count must be >=0"
        end=-1
        if count!=0:
            end=start+count-1
        return self.redis_inst.zrange(key,start,end,desc=reverse,withscores=score)

    """
    # function：获取sorted set结构成员的分数值[zscore]
    # return：  失败抛出异常，成功返回成员的分数值
    """
    def get_score_from_sorted_set(self,key,member):
        if key is None or member is None:
            raise ValueError("params invalid")
        res = self.redis_inst.zscore(key,member)
        #debug_log("Redis get_score_from_sorted_set, key=%s, member=%s, res=%s", key,str(member),str(res))
        return res

    """
    # function：获取sorted set结构的内容[zrevrangebyscore]
    # args:     闭合区间可选，startid:起始score(不包含startid传'(startid')，endid:结束score(不包含endid传'(endid')')')
    #           count:总数，count=0默认取整个有续集
    #           reverse默认按score倒序返回
    # return：  失败抛出异常，成功返回列表结构:[('v1',score1),('v2',score2)]
    """
    #------修改------
    def get_from_sorted_set_by_score(self,key,startid,endid,count=0,reverse=True):
        if key is None or startid is None or endid is None or count is None:
            raise ValueError("params invalid")
        assert count>=0, "count<0"
        if reverse:
            if count==0:
                return self.redis_inst.zrevrangebyscore(key,startid,endid,withscores=True)
            return self.redis_inst.zrevrangebyscore(key,startid,endid,start=0,num=count,withscores=True)
        else:
            if count==0:
                return self.redis_inst.zrangebyscore(key,startid,endid,withscores=True)
            return self.redis_inst.zrangebyscore(key,startid,endid,start=0,num=count,withscores=True)
        return

    """
    # function：删除sorted set结构的val内容[zrem]
    # args:     删除的元组val
    # return：  失败抛出异常，成功则删除数据且无异常抛出
    """
    def del_from_sorted_set(self,key,*val_args):
        if key is None or val_args is None or not val_args:
            raise ValueError("params invalid")
        #debug_log("Redis del_from_sorted_set, key=%s, val=%s", key, str(val_args))
        self.redis_inst.zrem(key,*val_args)

    """
    # function：通过score删除sorted set结构的val内容[zremrangebyscore](删除单个score)
    # args:     欲删除的分数score
    # return：  失败抛出异常，成功则删除数据且无异常抛出
    """
    def del_from_sorted_set_by_score(self,key,score):
        if key is None or score is None:
            raise ValueError("params invalid")
        self.redis_inst.zremrangebyscore(key,score,score)

    """
    # function：通过score删除sorted set结构的val内容[zremrangebyscore]
    # args:     闭合区间可选，startid:起始score(不包含startid传'(startid')，endid:结束score(不包含endid传'(endid')
    # return：  失败抛出异常，成功则删除数据且无异常抛出
    """
    #------新添加------
    def del_from_sorted_set_by_section_score(self,key,startid,endid):
        if key is None or startid is None or endid is None:
            raise ValueError("params invalid")
        self.redis_inst.zremrangebyscore(key,startid,endid)

    """
    # function：通过下表删除sorted set结构的val内容[zremrangebyrank]
    # args:     start起始下标，end结束下标，end=-1表示最后一个元素的下标
    # return：  失败抛出异常，成功则删除数据且无异常抛出
    """
    #------新添加------
    def del_from_sorted_set_by_rank(self,key,start=0,end=-1):
        if key is None:
            raise ValueError("key invalid")
        self.redis_inst.zremrangebyrank(key,start,end)

    """
    # function：将内容以hashes结构存到cache[hset|hmset]
    # args:     field是hash表内的字段名，fieldval是字段值
    #            field和fieldval是一对，两者存在，则使用hset命令
    #            mapping结构：{'f1':v1,'f2':v2}，mapping存在则用hmset且直接忽略field内容
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def put_to_hash_cache(self, key, field=None, fieldval=None, mapping=None):
        if key is None:
            raise ValueError("key invalid")
        if field is not None and fieldval is not None:
            return self.redis_inst.hset(key, field, fieldval)
        if mapping is not None:
            return self.redis_inst.hmset(key, mapping)
        raise ValueError("params invalid")

    """
    # function：获取cache中以hashes结构存储的内容[hmget]
    # args:     field为字段key的元组列表
    # return：  失败抛出异常，成功返回列表类型，
    #            即field值对应的fieldval列表,对应的field不存在返回None
    """
    def get_from_hash_cache(self,key,*field):
        if key is None or field is None or not field:
            raise ValueError("params invalid")
        return self.redis_inst.hmget(key, *field)

    """
    # function：获取cache中以hashes结构存储的内容[hgetall]
    # return：  失败抛出异常，成功返回列表类型，不存在返回{}
    """
    def get_all_from_hash_cache(self,key):
        if key is None:
            raise ValueError("key invalid")
        res = self.redis_inst.hgetall(key)
        #debug_log("Redis get_all_from_hash_cache, key=%s,res=%s",key, str(res))
        return res
    
    """
        # function: 将内容以hashes结构存储到cache中
        # args:     field是hash表内的字段名，fieldval是字段值
        #           field和fieldval是一对，两者存在，则使用hset命令
        # timeout   是设置key的过期时间
        # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def put_to_hset_ex(self,key,field,value,timeout):
        if key is None or field is None or timeout is None:
            raise ValueError('params invalid')
        assert timeout > 0,'timeout must > 0'
        self.redis_inst.hset(key,field,value)
        self.redis_inst.expire((key,field),timeout)


    """
    # function：删除hashes结构的field内容[hdel]
    # args:     field_args为要删除的field字段元组，即可以多个field同时删除
    # return：  失败抛出异常，成功正常删除数据且无异常抛出
    """
    def del_from_hash_cache(self,key,*field_args):
        if key is None or field_args is None or not field_args:
            raise ValueError("params invalid")
        self.redis_inst.hdel(key, *field_args)

    """
    # function：将hashes结构的field内容自增[hincrby]
    # args:     field为hash字段，addnum为要自增的步长
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def atom_add_hash_field(self,key,field,addnum=1):
        if key is None or field is None:
            raise ValueError("params invalid")
        assert isinstance(addnum,int), "addnum must be int"
        self.redis_inst.hincrby(key,field,amount=addnum)

    """
    # function：将hashes结构的field内容自增[hincrbyfloat]
    # args:     field为hash字段，addnum为要增加的步长
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def atom_add_hash_field_by_float(self,key,field,addnum=1.0):
        if key is None or field is None:
            raise ValueError("params invalid")
        assert isinstance(addnum,float), "addnum must be float"
        self.redis_inst.hincrbyfloat(key,field,amount=addnum)

    """
    # function：将内容以set结构存到cache[sadd]
    # return：  失败抛出异常，成功正常写入数据且无异常抛出
    """
    def add_to_set_cache(self,key,*vallist):
        if key is None or vallist is None or not vallist:
            raise ValueError("params invalid")
        self.redis_inst.sadd(key,*vallist)

    """
    # function：删除以set结构存储的cache[srem]
    # return：  失败抛出异常，成功正常删除且无异常抛出
    """
    def del_from_set_cache(self,key,*vallist):
        if key is None or vallist is None or not vallist:
            raise ValueError("params invalid")
        self.redis_inst.srem(key,*vallist)

    """
    # function：获取set结构的内容[smembers]
    # return：  失败抛出异常
    #            成功返回set结构:set(['v1','v2']),不存在返回set([])
    """
    def get_from_set_cache(self,key):
        if key is None:
            raise ValueError("params invalid")
        return self.redis_inst.smembers(key)

    """
    # function：判断是否set集合中的一员[sismember]
    # return：  失败抛出异常
    #           成功返回False(非集合一员 or key不存在),True(存在成员)
    """
    def is_member_in_set_cache(self,key,val):
        if key is None or val is None:
            raise ValueError("params invalid")
        return self.redis_inst.sismember(key,val)

    def is_exists_key(self, key):
        if key is None:
            raise ValueError("params invalid")
        is_exist = self.redis_inst.exists(key)
        #debug_log("Redis is_exists_key, key=%s,is_exist=%s",key, str(is_exist))
        return is_exist

if __name__ == '__main__':
    _fn_ = "main"

    config_path = './cache.config'
    config_dic = {'host': '59.151.12.124', 'port': 6379, 'db': 0, 'max_conn': 5, 'timeout': 2} 
    cacheinterface = PY_Redis_Cache()
    #cacheinterface.init(config_path)
    cacheinterface.init(config_dic=config_dic)

    print(_fn_,"===========================string格式存储测试")
    try:
        res = cacheinterface.put_to_cache('foo1','aa')
        print _fn_,"1.put_to_cache",res,type(res)

        res = cacheinterface.put_to_cache_ex('foo2','bb',600)
        print _fn_,"2.put_to_cache_ex",res,type(res)

        res = cacheinterface.get_from_cache('foo1')
        print _fn_,"3.1、get_from_cache",res,type(res)
        res = cacheinterface.get_from_cache('foo2')
        print _fn_,"3.2、get_from_cache",res,type(res)

        reslist = cacheinterface.get_multi_from_cache('foo1','foo2')
        print _fn_,"4.get_multi_from_cache",reslist,type(reslist)

        res = cacheinterface.del_from_cache('foo1')
        print _fn_,"5.del_from_cache",res,type(res)

        reslist = cacheinterface.get_multi_from_cache('foo1','foo2')
        print _fn_,"6.get_multi_from_cache",reslist,type(reslist)

        print '--------------------mytest--------------------'
        res = cacheinterface.put_multi_to_cache(key1='aa',key2='bb')
        dic = {'key3':1122, 'key4':3344}
        res = cacheinterface.put_multi_to_cache(**dic)
        print _fn_,"mytest_1.0.put_to_cache",res,type(res)
        reslist = cacheinterface.get_multi_from_cache('key1','key2','key3','key4')
        print _fn_,"mytest_1.1.get_multi_from_cache",reslist,type(reslist)
        print '--------------------mytest--------------------'

    except Exception,e:
        print(_fn_,str(e))
        exit(-1)


    print(_fn_,"===========================sorted_set格式存储测试")
    c_s_key = "SORTED_SET_TEST"
    try:
        print(_fn_,"-----------------------1-------------------------")
        #增加sorted set格式内容
        res = cacheinterface.add_to_sorted_set(c_s_key,
                valist=[695230,120318,803933,321577,300792,405239,583001],
                sclist=[45,0,100,89,23,55,31])
        print _fn_,"1.add_to_sorted_set",res,type(res)

        print(_fn_,"-----------------------2-------------------------")
        #计算sorted set大小
        res = cacheinterface.get_num_from_sorted_set(c_s_key)
        print _fn_,"2.get_num_from_sorted_set",res,type(res)

        print(_fn_,"-----------------------3-------------------------")

        print '--------------------mytest--------------------'
        res = cacheinterface.get_from_sorted_set(c_s_key,0,0)
        print _fn_,"mytest_3.0 desc::get_from_sorted_set",res,type(res)
        res = cacheinterface.get_from_sorted_set(c_s_key,3,2)
        print _fn_,"mytest_3.1 desc::get_from_sorted_set",res,type(res)
        print '--------------------mytest--------------------'

        #倒序获取数据,根据start-count获取
        res = cacheinterface.get_from_sorted_set(c_s_key,0,10)
        print _fn_,"3.1 desc::get_from_sorted_set",res,type(res)
        #升序获得数据,根据start-count获取
        res = cacheinterface.get_from_sorted_set(c_s_key,0,5,False)
        print _fn_,"3.2 asc::get_from_sorted_set",res,type(res)

        print(_fn_,"-----------------------4-------------------------")
        #score::倒序获取数据(包括边界点值也返回，即89和23的分值内容也返回)
        res = cacheinterface.get_from_sorted_set_by_score(c_s_key,89,23,5)
        print _fn_,"4.1 desc::get_from_sorted_set_by_score",res,type(res)
        #score::升序获得数据
        res = cacheinterface.get_from_sorted_set_by_score(c_s_key,23,89,5,False)
        print _fn_,"4.2 asc::get_from_sorted_set_by_score",res,type(res)

        print '--------------------mytest--------------------'
        #res = cacheinterface.del_from_sorted_set_by_rank(c_s_key,0,2)
        res = cacheinterface.del_from_sorted_set_by_section_score(c_s_key,0,'(55')
        print _fn_,"mytest_3.1 desc::del",res,type(res)
        res = cacheinterface.get_num_from_sorted_set_by_score(c_s_key,'89',sys.maxint)
        print _fn_,"mytest_3.1 desc::get_num_from_sorted_set_by_score",res,type(res)
        res = cacheinterface.get_from_sorted_set_by_score(c_s_key,'(89',-sys.maxint,0)
        print _fn_,"mytest_3.1 desc::get_from_sorted_set_by_score",res,type(res)
        res = cacheinterface.get_from_sorted_set_by_score(c_s_key,'89','(100',0,reverse=False)
        print _fn_,"mytest_3.1 desc::get_from_sorted_set_by_score",res,type(res)
        print '--------------------mytest--------------------'

        print(_fn_,"-----------------------5-------------------------")
        #通过val删除数据
        res = cacheinterface.del_from_sorted_set(c_s_key,120318)
        print _fn_,"5.1 del_from_sorted_set",res,type(res)
        #通过score删除数据
        res = cacheinterface.del_from_sorted_set_by_score(c_s_key,45)
        print _fn_,"5.2 del_from_sorted_set_by_score",res,type(res)
        #删除后获取最终数据
        res = cacheinterface.get_from_sorted_set(c_s_key,0,10)
        print _fn_,"5.3 after_del::get_from_sorted_set",res,type(res)

        print(_fn_,"-----------------------6-------------------------")
        res = cacheinterface.get_score_from_sorted_set(c_s_key,300792)
        print _fn_,"6.get_score_from_sorted_set",res,type(res)
    except Exception,e:
        print(_fn_,str(e))
        exit(-1)


    print(_fn_,"===========================其他redis命令测试")
    try:
        #设置key过期时间
        res = cacheinterface.set_key_expire(c_s_key,120)
        print _fn_,"1.set_key_expire",res,type(res)
        #自增id
        c_incr_key = "INCR_TEST"
        res = cacheinterface.incr_key(c_incr_key)
        print _fn_,"2.1、incr_key",res,type(res)
        #获取自增id结果
        res = cacheinterface.get_from_cache(c_incr_key)
        print _fn_,"2.2、get_incr_key",res,type(res)
        #直接获取一个redis句柄
    except Exception,e:
        print(_fn_,str(e))
        exit(-1)


    print(_fn_,"===========================hash结构存储测试")
    try:
        c_h_key = "HASH_TEST"
        atom_field = "r-333"
        print(_fn_,"-----------------------1-------------------------")
        #hash写入
        res = cacheinterface.put_to_hash_cache(c_h_key,'r-1456121',1)
        print _fn_,"1.1 put_to_hash_cache",res,type(res)
        res = cacheinterface.put_to_hash_cache(c_h_key,'m-1456121',"mask_right")
        print _fn_,"1.2 put_to_hash_cache",res,type(res)
        res = cacheinterface.put_to_hash_cache(c_h_key,\
                            mapping={'r-333':0,"m-333":"mask333"})
        print _fn_,"1.3 put_to_hash_cache",res,type(res)

        print(_fn_,"-----------------------2-------------------------")
        # hget单个取方式
        res = cacheinterface.get_from_hash_cache(c_h_key,\
                                        'r-1456121','m-1456121')
        print _fn_,"2.1 get_from_hash_cache",res,type(res)
        res = cacheinterface.get_all_from_hash_cache(c_h_key)
        print _fn_,"2.2 get_all_from_hash_cache",res,type(res)

        print(_fn_,"-----------------------3-------------------------")
        res = cacheinterface.del_from_hash_cache(c_h_key,'r-1456121','m-1456121')
        print _fn_,"3. del_from_hash_cache",res,type(res)

        print(_fn_,"-----------------------4-------------------------")
        res = cacheinterface.atom_add_hash_field(c_h_key,'r-333',addnum=5)
        print _fn_,"4.1 atom_add_hash_field",res,type(res)
        res = cacheinterface.get_all_from_hash_cache(c_h_key)
        print _fn_,"4.2 after_all::get_all_from_hash_cache",res,type(res)
        #cacheinterface.atom_add_hash_field_by_float('RH:1001','float-333',addnum=1.5)
    except Exception,e:
        print(_fn_,str(e))
        exit(-1)


    print(_fn_,"===========================set结构存储测试")
    try:
        c_set_key = "SET_TEST"
        res = cacheinterface.add_to_set_cache(c_set_key,'a','b','c',1,2,3)
        print _fn_,"1.add_to_set_cache",res,type(res)

        res = cacheinterface.get_from_set_cache(c_set_key)
        print _fn_,"2.get_from_set_cache",res,type(res)

        res = cacheinterface.del_from_set_cache(c_set_key,'a',3,'d')
        print _fn_,"3.del_from_set_cache",res,type(res)

        res = cacheinterface.get_from_set_cache(c_set_key)
        print _fn_,"4. after_all::get_from_set_cache",res,type(res)

        res = cacheinterface.is_member_in_set_cache(c_set_key,'a')
        print _fn_,"5.1. is_member_in_set_cache(not exist)",res,type(res)

        res = cacheinterface.is_member_in_set_cache(c_set_key,2)
        print _fn_,"5.2. is_member_in_set_cache(exist)",res,type(res)

        res = cacheinterface.is_member_in_set_cache("ddddddd",'b')
        print _fn_,"5.3. is_member_in_set_cache(no cache key)",res,type(res)
    except Exception,e:
        print(_fn_,str(e))
        exit(-1)

    exit(0)

