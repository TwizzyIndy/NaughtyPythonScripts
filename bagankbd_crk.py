#!/usr/bin/env python

"""

 author : TwizzyIndy
 date : 11/2018
 description : frida script for BaganKeyboard (Android)

"""

import frida
import sys


package_name = "com.bit.androsmart.kbinapp"

def get_messages_from_js(message, data):
            print(message)

jsc = """

Java.perform(function () {

    var scheduleJob = Java.use('jobs.ScheduleJob');
    scheduleJob.$init.implementation = function(u) {
        send('$init');
        this.$init(u);
        this.mShowPremium = true;
        
    }
    
    scheduleJob.access$1200.implementation = function(x) {
        send('access$1200');
        return true;
    }
    
    scheduleJob.checkPremium.implementation = function(arg1, arg2) {
        send('checkPremium');
        //this.checkPremium(arg1, arg2);
        console.log("checkPremium : arg1 : " + arg1);
        return true;
    }
})


"""

process = frida.get_usb_device().attach(package_name)
script = process.create_script(jsc)
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()