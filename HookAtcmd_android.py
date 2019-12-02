"""

Frida Hooking Script for Huawei ATCMDSERVER

Author      : TwizzyIndy
Date        : 12/2018
Description :
Usage       : 

"""

import frida
import frida_tools
import os
import sys


processname = "atcmdserver"

def get_messages_from_js(message, data):
    print(message)
    

jsc = """

// https://awakened1712.github.io/hacking/hacking-frida/

function memAddress(memBase, idaBase, idaAddr) {
    var offset = ptr(idaAddr).sub(idaBase);
    var result = ptr(memBase).add(offset);
    return result;
}

function idaAddress(memBase, idaBase, memAddr) {
    var offset = ptr(memAddr).sub(memBase);
    var result = ptr(idaBase).add(offset);
    return result;
}

membase = Module.findBaseAddress('atcmdserver');

genRandomBytesFunc = memAddress(membase, '0x0', '0x35FF0');
generateSeedFunc = memAddress(membase, '0x0', '0x37534');
genSeedViaSecretMatrix = memAddress(membase, '0x0', '0x371CC');

// Generate Random Secret Bytes Function (4Bytes)
// genRandomBytesFunc

// signed __int64 __fastcall GenerateSeed(__int64* secret, unsigned __int16 secretLen, 
// __int64* seedHex, __int64 &a4, _DWORD *pTable_a5);

Interceptor.attach(genRandomBytesFunc, {
    
    onEnter: function(args)
    {
       //console.log("genRandomBytesFunc: entered");
       
    },
    
    onLeave: function(retval)
    {
       // not effect changing values here !
       // TODO: better research
    }

});

// Generate Seed Function

Interceptor.attach(generateSeedFunc, {

    onEnter: function(args)
    {
        //Memory.writeInt(args[0], 0xFFDD8932); // it works
        
        //console.log("GenerateSeed : ");
        //console.log("arg1 secret : " + Memory.readInt(args[0]).toString());
        //console.log("arg2 secretLen : " + args[1].toString());
        
        //console.log("arg3 outputSeedHex : " + args[2].toString());
        //console.log("arg4 outputSeedLen : " + args[3].toString());
        //console.log("arg5 Table : " + args[4].toString());
        
    },
    
    onLeave: function(retval)
    {
        
    }

});

// genSeedViaSecretMatrix

// signed __int64 __fastcall GenSeedViaSecretMatrix(__int64* inputKeyHex, 
// unsigned __int16 inputKeyLen, 
// __int64& p_Cipher, 
// _WORD *a4, _DWORD *table);

var g_outputKeyLenPtr = 0x0;
var g_outputKeyPtr = 0x0;
var g_tablePtr = memAddress(membase, '0x0', '0x69E5C'); //'0x69D58' + 260);
var g_tablePtr1 = memAddress(membase, '0x0', '0x69D58');

Interceptor.attach(genSeedViaSecretMatrix, {

     onEnter: function(args)
     {
         //var inputKeyLen = args[1].toInt32();
         //g_outputKeyLenPtr = args[3];
         //g_outputKeyPtr = args[2];
         
         /*
         console.log("GenSeedViaSecretMatrix : ");
         console.log("inputKeyHex : " + hexdump(Memory.readByteArray(args[0], inputKeyLen),{
            offset: 0,
            length: 128,
            header: true,
            ansi: false
         }));
         */
         
     },
     
     onLeave: function(retval)
     {
         /*
         console.log("output len : " + Memory.readS16(g_outputKeyLenPtr));
         var outputLen = Memory.readS16(g_outputKeyLenPtr);
         
         var outputPtr = g_outputKeyPtr;
         
         console.log("GenSeedViaSecretMatrix onLeave:");
         console.log("output :" + hexdump(Memory.readByteArray(outputPtr, outputLen), {
             offset: 0,
             length: outputLen,
             header: true,
             ansi: false
         }));
         */
     }

});

// hex string array to binary bytes array
function parseHexString(str) { 
    var result = [];
    while (str.length >= 2) { 
        result.push(parseInt(str.substring(0, 2), 16));
        str = str.substring(2, str.length);
    }

    return result;
}
// byte array to hex string
function byte2hex(byteArray)
{
   var result = '';
   for(var i=0; i !== byteArray.length; i++)
   {
     result += byteArray[i].toString(16);
   }
   return result;
}

function addSecret(str)
{
   var result = [];
   result[0] = 0x0;
   result[1] = 0x1;
   
   for( var i = 2; i < 128; i++ )
   {
       result[i] = 0xFF;

       
       if( i == 123 )
       {
           result[i] = 0x0;
           break;
       }
   }
   while(str.length != 0)
   {
      result.push(parseInt(str.substring(0, 2), 16));
      str = str.substring(2, str.length);
   }
   return result;
}

function reverseStr(str)
{
    var newStr = "";
    
    for(var i = str.length - 1; i >= 0; i -= 8 )
    {
        firstByte = str[i-7] + str[i-6];
        secByte = str[i-5] + str[i-4];
        thirdByte = str[i-3] + str[i-2];
        fourthByte = str[i-1] + str[i];
        
        newStr += firstByte + secByte + thirdByte + fourthByte;
    }
    return newStr;
}

// need to be little-endian bytes array
// FIXME:
function encrypt(strMagic)
{
    var callGenseedViaSecretMatrix = new NativeFunction(genSeedViaSecretMatrix, 'int64', ['pointer', 'int16', 'pointer', 'pointer', 'pointer']);
    var returnValue = 0;
    
    var sec = "0001FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00";
    sec = sec + strMagic;
    //sec = reverseStr(sec);
    
    var secPtr = Memory.alloc(128);
    var secHexPtr = parseHexString(sec);
    
    //console.log("secHexArray : " + secHexPtr);

    Memory.writeByteArray(secPtr, secHexPtr);
    
    
    var nOutputKeyPtr = Memory.alloc(128);
    var nOutputKeyLenPtr = Memory.alloc(2);

    returnValue = callGenseedViaSecretMatrix(secPtr, 128, nOutputKeyPtr, nOutputKeyLenPtr, g_tablePtr );
    console.log("myNativeCall returned : " + returnValue.toString());
    
    var outputLen = Memory.readS16(nOutputKeyLenPtr);
         
    var outputPtr = nOutputKeyPtr;

    console.log("outputLen : " + outputLen.toString());

    console.log("output :" + hexdump(Memory.readByteArray(outputPtr, outputLen), {
             offset: 0,
             length: outputLen,
             header: true,
             ansi: false
         }));
}



function decrypt(strHex)
{
    var callGenseedViaSecretMatrix = new NativeFunction(genSeedViaSecretMatrix, 'int64', ['pointer', 'int16', 'pointer', 'pointer', 'pointer']);
    var returnValue = 0;
    
    var decStr = strHex;
    var decHexArr = parseHexString(decStr);
    
    var nInputKey = Memory.alloc(128);
    Memory.writeByteArray(nInputKey, decHexArr);

    var nOutputKeyPtr = Memory.alloc(128);
    var nOutputKeyLenPtr = Memory.alloc(2);

    returnValue = callGenseedViaSecretMatrix(nInputKey, 128, nOutputKeyPtr, nOutputKeyLenPtr, g_tablePtr );
    console.log("myNativeCall returned : " + returnValue.toString());
    
    var outputLen = Memory.readS16(nOutputKeyLenPtr);
         
    var outputPtr = nOutputKeyPtr;

    console.log("outputLen : " + outputLen.toString());

    console.log("output :" + hexdump(Memory.readByteArray(outputPtr, outputLen), {
             offset: 0,
             length: outputLen,
             header: true,
             ansi: false
         }));
         
    key = [];
    bAr = Memory.readByteArray(outputPtr, outputLen);
    
    if( bAr.length == 0 || bAr.length == NULL )
    {
         return "cant decrypted";
    }
    
    for(var i=124; i <= bAr.length; i++)
    {
        key.push( bAr[i] );
    }
    
    console.log(byte2hex(key));
}

// NOTES : default seed given on csdn : decrypted cipher is 0xD11E81E7

encrypt("D11E81E7")

// call decrypt
//var x = reverseStr("59571792c111dbac7e5856ecf1206f0794db9c6b02d6ec33b0636f56d3b22e3c90150763a3414bf79c2945038948ee5e5f80ee0a858c82a6b68740c772d717856b0ae977fb1f5b00b8f79ee605b8a6cd8afa6d640a791452b839f6cfdc5d66a12d850bc5aab9aa9b7c9f0ce685345670dffa13474596275cd355886c5fce84ad");
//console.log("reversed : " + x);


// atcmdserver.py :decrypt("aa06c7b48dd42909926e8223f34aed30baea9bbe44926d818aa81464f5178150a66da672483cbab08a13cc7240d85066878c2a640c4cf26f3d8a8b6969d0a788304bab1dd567fe80bc6c1ca170eda312af3cb0089f12bdde014dd2a0d516526e8ac403a112ec81e20f3f692dc3d7abb590c2b312613422d6a734817310732125");



"""

def main():
    
    process = frida.get_usb_device().attach(processname)
    script = process.create_script(jsc )
    script.on('message',get_messages_from_js)
    script.load()
    #sys.stdin.read()
    
if __name__ == "__main__":
    main()