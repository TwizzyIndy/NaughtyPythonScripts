# author : TwizzyIndy
# date : 9/3/2018


import xxtea
import os
import sys
import struct

# decrypt , encrypt resource files for or.cocos2d.Lobby.apk

def _remove_header(str, sign):
    return str[len(sign):]

def _add_header(str, sign):
    return sign + str


def main():

    arg1 = os.sys.argv[1]
    arg2 = os.sys.argv[2]

    _xsign = b'5by5'
    _key = b'm2NkkPpfWJxmTvuV'
    CURRENT_EXT = ".xml"
    
    

    if arg1 == '-d':
        filein = arg2
        #fileout = arg2 + CURRENT_EXT
        fileDir, fileName = os.path.split(arg2)
        
        if str(fileDir) == "":
            fileDir = os.getcwd()
            
        if not os.path.exists(fileDir + "/xml"):
            os.mkdir(fileDir + "/xml")
        if not os.path.exists(fileDir + "/png"):
            os.mkdir(fileDir + "/png")
        if not os.path.exists(fileDir + "/luaj"):
            os.mkdir(fileDir + "/luaj")
        if not os.path.exists(fileDir + "/unknown"):
            os.mkdir(fileDir + "/unknown")
        if not os.path.exists(fileDir + "/zip"):
            os.mkdir(fileDir + "/zip")
        if not os.path.exists(fileDir + "/json"):
            os.mkdir(fileDir + "/json")

        with open(filein, 'rb') as raw:
            magic = raw.read(4)
            raw.seek(0)
            
            if magic == b'5by5':
                rawdata = raw.read()
                data = _remove_header(rawdata, _xsign)
                plain = xxtea.decrypt(data, _key)
                
                if bytes(plain).startswith(b'<?xml') == True: # XML
                    CURRENT_EXT = ".xml"
                    fileName += CURRENT_EXT
                    print("its xml\n")
                    with open( fileDir + "/xml/" + fileName, 'wb') as output:
                        output.write(plain)
                    #move it
                    
                        
                elif bytes(plain).startswith(b'\x89\x50\x4E\x47') == True: # PNG
                    CURRENT_EXT = ".png"
                    fileName += CURRENT_EXT
                    print("its png\n")
                    with open(fileDir + "/png/" + fileName, 'wb') as output:
                        output.write(plain)
                        
                elif bytes(plain).startswith(b'\x1B\x4C\x4A') == True: # LUA JIT
                    CURRENT_EXT = ".luaj"
                    print("its lua jit\n")
                    fileName += CURRENT_EXT
                    with open(fileDir + "/luaj/" + fileName, 'wb') as output:
                        output.write(plain)
                        
                elif bytes(plain).startswith(b'PK') == True: # ZIP
                    CURRENT_EXT = ".zip"
                    print("its zip")
                    fileName += CURRENT_EXT
                    with open(fileDir + "/zip/" + fileName, 'wb') as output:
                        output.write(plain)
                        
                elif bytes(plain).startswith(b'{"') == True: # JSON
                    CURRENT_EXT = ".json"
                    print("its json")
                    fileName += CURRENT_EXT
                    with open(fileDir + "/json/" + fileName, 'wb') as output:
                        output.write(plain)
                else:
                    
                    print("its unknown\n")
                    unknown_magic = bytes(plain)[:4]
                    print("magic : " + str(unknown_magic))
                    CURRENT_EXT = "_" + str(unknown_magic)
                    fileName += CURRENT_EXT
                    with open(fileDir + "/unknown/" + fileName, 'wb') as output:
                        output.write(plain)
                        
    elif arg1 == '-e':
        fileIn = arg2
        fileOut = arg2 + "_"

        with open(fileIn, 'rb') as raw:
            with open(fileOut, 'wb') as output:
                rawdata = raw.read()
                encrypted = xxtea.encrypt(rawdata, _key)
                datawithsign = _add_header(encrypted, _xsign)
                output.write(datawithsign)
    return

if __name__ == "__main__":
    main()