import os

DIR_ROOT = "/home/ming.ma/workspace/"
SUFFIX = ".py"


CONFIG_PATH = "./pyutil/tools/code_replace/example.config"
REPLACE = {
    "import pyutil.db.config.": "import pyconf.db.",
}

def parse(names = {}):
    if not os.path.exists(DIR_ROOT):
        print "Please check whether root dir exist."
    for rt, dirs, files in os.walk(DIR_ROOT):
        for name in files:
    	    path = rt+"/"+name
    	    print path
            if path.find("code_replace.py") >=0 or path.find("/.git/")>=0 :
                continue

    	    if not path.endswith(SUFFIX):
    	    	continue
    	    f = open(path, "r")
    	    content = f.read()
    	    f.close()

            for k in sorted(REPLACE.keys()):
                content = content.replace(k, REPLACE[k])

    	    f = open(path, "w")
    	    f.write(content)
    	    f.close()

def init():
    f = open(CONFIG_PATH)
    for line in f.readlines():
        items = line.strip().split()
        if len(items) != 2:
            continue
        else:
            REPLACE[items[0]] = items[1]
    f.close()


if __name__ == '__main__':
    init()
    parse()
