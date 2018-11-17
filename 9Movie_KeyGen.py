import os
import sys
import subprocess
import hashlib


def main():
    
    #uuid = str( subprocess.check_output('wmic csproduct get UUID') ).splitlines()[1]
    uuid = hashlib.md5('1780B0C2-0B42-FBDB-BDB0-047D7BF3C504').hexdigest()
    key = hashlib.md5('C6944266-693B-4F2B-B4F1-ACA2A9F24A4E').hexdigest()
    
    myMD5 = hashlib.md5( uuid + key ).hexdigest()
    
    VALID_CHAR = "0123456789ABCDEFGHJKLMNPQRTUVWXY"
    sn = ''
    
    for x in range(16):
        by = myMD5[x*2:2]
        
        ch = int( by, 16 ) % 32
        sn += VALID_CHAR[ch:1]
        
    print( sn )
    
    return

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]), 16)

if __name__ == "__main__":
    main()