#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib2
import sys
import json

def Request(url, up_data=None, method="GET", headers=None, timeout=5, repeated=1, content_type="application/json", raised=False):
    url =  url if url.startswith("http") else "http://"+url
    for i in range(repeated):
        req = None
        try:
            if method=="GET":  #GET
                if headers:
                    req = urllib2.Request(url, headers=headers)
                else:
                    req = urllib2.Request(url)
                return urllib2.urlopen(req).read()
            elif method.upper() in ["POST", "PUT", "DELETE"]:   #POST, PUT, DELETE
                if isinstance(up_data, unicode):
                    up_data = up_data.encode('utf-8')
                elif isinstance(up_data, list) or isinstance(up_data, dict) or isinstance(up_data, tuple):
                    up_data = json.dumps(up_data)
                if not headers:
                    headers = {'Content-Type': content_type}
                req = urllib2.Request(url, headers=headers, data=up_data)
                req.get_method = lambda: method.upper()
                response = urllib2.urlopen(req, timeout=timeout)
                return response.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'Failed to reach a server, Reason: ', e.reason
            if hasattr(e, 'read'):
                print 'Error code: ', e.code
        except Exception, e:
            print "Exception:", e
    print >> sys.stderr, "Failed to vist:", url
    return None


def PostJson(url, data):
    if isinstance(data, list) or isinstance(data, dict) or isinstance(data, tuple):
        data = json.dumps(data)
    response = Request(url, data, method="POST", headers={'Content-Type':"application/json"})
    return response


def PostUrlencoded(url, fieldsMap):
    postData = "&".join([str(k)+"="+str(v) for k,v in fieldsMap.items()])
    response = Request(url, postData, method="POST", headers={'Content-Type':"application/x-www-form-urlencoded"}, repeated=3)
    return response

def PostFormData(url , fieldsMap):  
    BOUNDARY = '----------Th0s_1s_tHe_fub119RY_$'  
    def encode_multipart_formdata( fieldsMap ):  
        CRLF = '\r\n'  
        L = []  
    
        for key, val in fieldsMap.items():
            L.append( '--' + BOUNDARY )  
            L.append( 'Content-Disposition: form-data; name="%s"' % key )  
            L.append( '' )
            L.append( val )
    
        L.append( '--' + BOUNDARY + '--' )
        L.append( '' )
        body = CRLF.join( L )
        return body

    def gen_req(fieldsMap):
        body = encode_multipart_formdata( fieldsMap )

        req = urllib2.Request( url, body )
        req.add_header( "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0)" )
        req.add_header( "Accept", "*/*" )
        req.add_header( "Accept-Language", "zh-CN,zh;q=0.8" )
        req.add_header( "Accept-Encoding", "gzip,deflate,sdch" )
        req.add_header( "Connection", "keep-alive" )
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        #content_type = 'application/x-www-form-urlencoded; boundary=%s' % BOUNDARY  
        req.add_header( "Content-Type", content_type )  
        req.add_header( "User-Agent1", "SogouMSE" )  
        return req

    try:  
        req = gen_req(fieldsMap)
        response = urllib2.urlopen( req ).read().decode( 'utf-8' )  
        return response  
    except urllib2.HTTPError, e:  
        print e.code
    except urllib2.URLError, e:  
        print str( e )  
    except Exception,e:
        print "Exception,e:", e


if __name__ == '__main__':
    print Request('www.baidu.com')
