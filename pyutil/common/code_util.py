
import re

def isVarName(s):
    results = re.findall('^[0-9A-Za-z_]+$',s)
    return True if len(results)>0 else False
