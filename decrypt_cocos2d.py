#!/usr/bin/env python

"""

 author : TwizzyIndy
 date : 3/2018
 description : frida script for MonstersRevenge2 (Android)

"""

import frida
import sys

# _Z13xxtea_decryptPhjS_jPj

# cipher : m2NkkPpfWJxmTvuV
# sign : 5by5


# luaL_loadBuffer(lua_State *, char const*, int, char const*)

package_name = "org.cocos2dx.Lobby"

def get_messages_from_js(message, data):
            print(message)

jsc = """

// Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "fish_sim_tick"),
// {
//     onEnter: function(args) {

//         console.log("--------- START ------------");
//         console.log(hexdump(Memory.readByteArray(args[1], 16),{
//             offset: 0,
//             length: 16,
//             header: true,
//             ansi: true
//         }));

//         //console.log( "fish_sim_tick arg2 : " + Memory.readByteArray(args[1], 32).toString());

//     },

//     onLeave: function(retval) {
//         console.log( "fish_sim_tick retval : " + Memory.readInt(retval).toString());
//         console.log("--------- END ------------");
//     }
// });

var isFound = false;

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "lua_getfield"),
{
    onEnter: function (args) {

        var str = Memory.readUtf8String(args[2]);


        if( str.includes("tick") )
        {

            // var arg1 = args[1].toString();

            // console.log("----------------BEGIN----------------");
            // console.log("lua_getfield:");
            // console.log("arg1(L_stack): " + args[0].toString());
            // console.log("arg2(index) : " + arg1);
            // console.log("arg3(name) : " + str);

            isFound = true;
            // get function pointers
            //var checkinteger = Module.findExportByName("libcocos2dlua.so", "luaL_checkinteger");
            //var setfield = Module.findExportByName("libcocos2dlua.so", "lua_setfield");

            //var ptrCheckInt = checkinteger.toString();
            //var ptrSetField = setfield.toString();
            //console.log("checkinteger: " + ptrCheckInt);
            //console.log("setfield: " + ptrSetField);
            
            // set native functions
            //var funcCheckInteger = new NativeFunction(ptr(checkinteger.toInt32()), 'int', ['pointer', 'int']);
            //var funcSetField = new NativeFunction(ptr(ptrSetField), 'pointer', ['pointer', 'int', 'pointer']);

            //var strPos = funcCheckInteger(ptr(args[0].toInt32()), 4);
            //console.log("-> : " + strPos.toString() ) ;
        } else {
            isFound = false;
        }

    },

    onLeave: function(retval){

        //console.log(Memory.readInt(retval).toString());
        if( isFound )
        {
            // console.log("-----------------END-----------------");
        }
    }
    
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "lua_setfield"),
{
    onEnter: function (args) {

        var str = Memory.readUtf8String(args[2]);

        if( str.includes("tick") )
        {
            isFound = true;
            // var arg1 = args[1].toString();

            // console.log("----------------BEGIN----------------");
            // console.log("lua_setfield:");
            // console.log("arg1(L_stack): " + args[0].toString());
            // console.log("arg2(index) : " + arg1);
            // console.log("arg3(name) : " + str);

            
        } else {
            isFound = false;
        }

    },

    onLeave: function(retval){
        if( isFound )
        {
            //console.log(Memory.readInt(retval).toString());
            // console.log("-----------------END-----------------");
        }

    }
    
});

Interceptor.attach(Module.findExportByName("libcocos2dlua.so", "fish_sim_point_query"), 
{
    onEnter: function(args)
    {
        //console.log("----- BEGIN ------");
        //console.log("fish_sim_point_query : ");
        //console.log("arg1 : " + args[0].toString());
        //console.log("arg2 : " + args[1].toString());
        //console.log("arg3 : " + args[2].toString());

    },

    onLeave: function(retval)
    {
        // console.log(hexdump(Memory.readByteArray(retval, 32),{
        //     offset: 0,
        //     length: 32,
        //     header: true,
        //     ansi: true
        // }));
        // console.log("----- END  ------");
    }
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "lua_pushinteger"),
{
    onEnter: function (args) {

        if( isFound )
        {

            var strInt = args[1]; //args[1].toString();

            // console.log("----------------BEGIN----------------");
            // console.log("lua_pushinteger:");
            // console.log("arg1(L_stack): " + args[0].toString());
            // console.log("arg2(integer) : " + strInt.toString());

            if( strInt < 1000 )
            {
                args[1] = 1000;//args[1] + 800;
                // console.log("HACKED!!!!");
            }

        }
    },

    onLeave: function(retval){
        if( isFound )
        {
            //var ptrArg0 = Memory.readInt32(args[0]);
            //console.log("arg1 : " + ptrArg0);
            //console.log("retval : " + Memory.readInt(retval).toString());
            // console.log("-----------------END-----------------");
        }
    }
    
});


/*
Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "luaL_loadbuffer"),
{
    onEnter: function (args) {

        console.log("----------------BEGIN----------------");
        console.log("luaLoadBuffer:");
        

        console.log("arg2(data) : ");
        console.log(hexdump(Memory.readByteArray(args[1], 32),{
            offset: 0,
            length: 32,
            header: true,
            ansi: true
        }));

        
        console.log("arg3(fileName) : ");
        console.log(hexdump(Memory.readByteArray(args[3], 32),{
            offset: 0,
            length: 32,
            header: true,
            ansi: true
        }));
        
        console.log("-----------------END-----------------");       

    },

    onLeave: function(retval){

    }
    
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "luaL_loadfilex"),
{
    onEnter: function (args) {

        console.log("----------------BEGIN----------------");
        console.log("luaL_loadfilex:");
        

        console.log("arg2(filename) : ");
        console.log(hexdump(Memory.readByteArray(args[1], 32),{
            offset: 0,
            length: 32,
            header: true,
            ansi: true
        }));

        
        console.log("arg3(fileName) : ");
        console.log(hexdump(Memory.readByteArray(args[3], 32),{
            offset: 0,
            length: 32,
            header: true,
            ansi: true
        }));
        
        console.log("-----------------END-----------------");       

    },

    onLeave: function(retval){

    }
    
});
*/

/*
Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "_Z13xxtea_encryptPhjS_jPj"), 
{
    
onEnter: function (args) {
    console.log("----------------BEGIN----------------");
    console.log("Key:");
    console.log(hexdump(Memory.readByteArray(args[2], 12),{
        offset: 0,
        length: 12,
        header: true,
        ansi: true
    }));
},

    onLeave: function (retval) {
        console.log("Encrypted:");
        console.log(hexdump(Memory.readByteArray(retval, 16),{
         offset: 0,
         length: 16,
         header: true,
         ansi: true
        }));
        
        console.log("-----------------END-----------------");   
    }
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "_ZN7cocos2d8LuaStack18setXXTEAKeyAndSignEPKciS2_i"), 
{
    
onEnter: function (args) {
    console.log("----------------BEGIN----------------");
    console.log("setXXTEAKeyAndSignEPK:");
    console.log("key:");
    console.log(hexdump(Memory.readByteArray(args[1], 12),{
        offset: 0,
        length: 12,
        header: true,
        ansi: true
    }));

    console.log("sign:");
    console.log(hexdump(Memory.readByteArray(args[3], 12),{
        offset: 0,
        length: 12,
        header: true,
        ansi: true
    }));
},
    onLeave: function (retval) {
        //console.log("Encrypted:");
        //console.log(hexdump(Memory.readByteArray(retval, 16),{
        // offset: 0,
        // length: 16,
        // header: true,
        // ansi: true
        //}));
        
        console.log("-----------------END-----------------");   
    }
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "_Z13xxtea_encryptPhjS_jPj"), 
{
    
onEnter: function (args) {
    console.log("----------------BEGIN----------------");
    console.log("Key:");
    console.log(hexdump(Memory.readByteArray(args[2], 12),{
        offset: 0,
        length: 12,
        header: true,
        ansi: true
    }));
},

    onLeave: function (retval) {
        console.log("Encrypted:");
        console.log(hexdump(Memory.readByteArray(retval, 16),{
         offset: 0,
         length: 16,
         header: true,
         ansi: true
        }));
        
        console.log("-----------------END-----------------");   
    }
});

Interceptor.attach (Module.findExportByName( "libcocos2dlua.so", "_Z13xxtea_decryptPhjS_jPj"), 
{
    
onEnter: function (args) {
    console.log("----------------BEGIN----------------");
    console.log("Key:");
    console.log(hexdump(Memory.readByteArray(args[2], 16),{
        offset: 0,
        length: 16,
        header: true,
        ansi: true
    }));
},

    onLeave: function (retval) {
        console.log("Decrypted:");
        console.log(hexdump(Memory.readByteArray(retval, 16),{
         offset: 0,
         length: 16,
         header: true,
         ansi: true
        }));
        
        console.log("-----------------END-----------------");   
    }
});

*/


"""

process = frida.get_usb_device().attach(package_name)
script = process.create_script(jsc)
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()