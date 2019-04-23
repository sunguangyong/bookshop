
import json
import pyutil.common.http_util as http_util
#import pyutil.gaode.disney_locations as locations


def main():
    key="7eba39d9b574ba7eafaa2053f891608a"
    url = "http://restapi.amap.com/v3/assistant/coordinate/convert?locations={0},{1}&coordsys=gps&output=json&key={2}"
    f = open("./pyutil/gaode/1208.txt")
    
    for line in f.readlines():
        item = line.split()
        a = "%.6f" % (float(item[0]))
        b = "%.6f" % (float(item[1]))

        u = url.format(a, b, key)
        data = http_util.Request(u)
        obj = json.loads(data)
        print "[%s, %s] : %s" % (item[0], item[1], obj["locations"])

if __name__ == '__main__':
    main()
