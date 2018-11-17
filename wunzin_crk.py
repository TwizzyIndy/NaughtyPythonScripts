#!/usr/bin/env python

"""

 author : TwizzyIndy
 date : 11/2018
 description : frida script for WunZin (Android)

"""

import frida
import sys


package_name = "com.bit.wunzin"

def get_messages_from_js(message, data):
            print(message)

jsc = """

Java.perform(function () {

    var bookOrder = Java.use('com.bit.wunzin.objects.BookOrder');
    var bookDetail= Java.use('com.bit.wunzin.fragments.addon.BookDetail');
    
    bookDetail.a.implementation = function(arg1, arg2) {
       send('a');
       console.log("BookDetail : " + arg1);
       this.a(arg1, arg2);
       
       
    }
    
    bookOrder.a.implementation = function(u) {
        send('a');
        //this.checkPremium(arg1, arg2);
        console.log("BookOrder : entered");
        return 1;
    }
})


"""

process = frida.get_usb_device().attach(package_name)
script = process.create_script(jsc)
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()