# -*- coding: UTF-8 -*-
"""
Camera library for scripts.
"""

import sys
import os
import re
import common
import time
from common import Common
from automator.adb import Adb

libpath = sys.path[0] + "\\..\\common"
sys.path.append(libpath)

settings_package = "com.android.settings"
settings_activity = "com.android.settings.Settings"


class Reboot(Common):
    def is_start(self):            
            environ = os.environ
            #self.logger.info("%s  " %environ)			
            device_id = environ.get("Mdevice")     
            self.logger.info("device_id is %s  " %device_id)
            self.device.delay(1)
            getData = self.device.server.adb.shell("getprop ro.serialno")             
            data = str(getData)
            if device_id in data :
                self.logger.info("reboot success")
                return True            
            else:
                self.logger.info("reboot failed")
                return False

    def test_reboot(self):        
        self.logger.info('soft reboot')        
        self.device.delay(1)        
        try:
            self.logger.info("begin reboot...")
            self.device.delay(3)
            self.device.server.adb.shell("reboot")
            self.device.delay(60)
            for i in range(120):
                self.device.delay(1)
                self.logger.info("%s " %i)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    self.logger.info("%s " %i)
                    return 
            return True
        except Exception,e:
            self.logger.debug(e)
            self.save_fail_img()
            
    def test_time_reboot(self):
        self.logger.info('soft time reboot')        
        self.device.delay(1)        
        try:
            self.logger.info("begin time reboot...")
            self.device.delay(3)
            self.device.server.adb.shell("monkey -f /sdcard/scriptlog.txt")
            self.device.delay(60)
            for i in range(120):
                self.device.delay(1)
                self.logger.info("%s " %i)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    self.logger.info("%s " %i)
                    return 
            return True
        except Exception,e:
            self.logger.debug(e)
            self.save_fail_img() 
            
    def test_longclick_reboot(self):
        self.device.delay(1)
        self.logger.info("longclick reboot...")	
        try:
            self.logger.info("begin reboot...")
            self.device.delay(3)
            a=os.system(libpath+"\\restart.bat")
            self.logger.info("return:%s" % a)
            
            if self.device(resourceId="android:id/reboot_layout").wait.exists(timeout=5000):
                self.logger.info("reboot_layout is exists")
                self.device(resourceId="android:id/reboot_layout").click()
            else:
                self.logger.info("reboot_layout is not exists")
                return False
            self.device.delay(60)
            for i in range(120):
                self.device.delay(1)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    return
            return True
            self.logger.info("Trace Success Loop %s." % (loop+1))
            self.suc_times = self.suc_times + 1
        except Exception,e:
            self.logger.debug(e)
            self.save_fail_img()  
            
    def test_longclick_withMemoryFull_reboot(self):
        self.device.delay(1)
        self.logger.info("longclickwithMemoryFull reboot...")	
        try:
            self.logger.info("begin reboot...")
            self.device.delay(3)		                
            os.system(libpath+"\\restart.bat")
            if self.device(resourceId="android:id/reboot_layout").wait.exists(timeout=5000):
                self.logger.info("reboot_layout is exists")
                self.device(resourceId="android:id/reboot_layout").click()
            else:
                self.logger.info("reboot_layout is not exists")
                return False
            self.device.delay(60)
            for i in range(120):
                self.device.delay(1)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    return
            return True 
            self.logger.info("Trace Success Loop %s." % (loop+1))
            self.suc_times = self.suc_times + 1
        except Exception,e:
            self.logger.debug(e)
            self.save_fail_img()
            
    def test_longclick_withContactsFull_reboot(self):
        self.device.delay(1)
        self.logger.info("longclickwithContactsFull reboot...")	
        try:
            self.logger.info("begin reboot...")
            self.device.delay(3)                
            os.system(libpath+"\\restart.bat")
            if self.device(resourceId="android:id/reboot_layout").wait.exists(timeout=5000):
                self.logger.info("reboot_layout is exists")
                self.device(resourceId="android:id/reboot_layout").click()
            else:
                self.logger.info("reboot_layout is not exists")
                return False
            self.device.delay(60)
            for i in range(120):
                self.device.delay(1)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    return
            return True 
            self.logger.info("Trace Success Loop %s." % (loop+1))
            self.suc_times = self.suc_times + 1
        except Exception,e:
            self.logger.debug(e)
            self.save_fail_img()  
            
    def test_auto_reboot(self):
        self.device.delay(1)
        self.logger.info("autore reboot...")	        
        self.back_to_home()
        self.device.delay(1)
        self.start_activity(settings_package, settings_activity)
        self.device.delay(1)
        if self.device(text="Date & time").exists:
            self.device(text="Date & time").click()
        else:
            self.device(scrollable=True).scroll.vert.forward(steps=100)
            if self.device(text="Date & time").wait.exists(timeout = 10000):
                self.device(text="Date & time").click()
            else:
                self.device(scrollable=True).scroll.vert.forward(steps=100)
                if self.device(text="Date & time").wait.exists(timeout = 10000):
                    self.device(text="Date & time").click()
                else:
                    self.device(scrollable=True).scroll.vert.forward(steps=100)
                    if self.device(text="Date & time").wait.exists(timeout = 10000):
                        self.device(text="Date & time").click()
                    else:
                        return False
        if self.device(text="Set time").wait.exists(timeout=3000):
            self.device(text="Set time").click()
            self.device.delay(1)
            if self.device(description="7").wait.exists(timeout=3000):
                self.device(description="7").click()
                if self.device(description="0").wait.exists(timeout=3000):
                    self.device(description="0").click()
                    self.device.delay(1)
                    self.device(text="OK").click()
                    self.device.delay(1)
                    self.logger.debug("set time minute is true")
                else:
                    self.logger.debug("set time minute is not true")
                    return False
            else:
                self.logger.debug("set time hour is not true")
                return False
        else:
            self.logger.debug("set time is not find")
            return False        
                
                
            self.device.delay(2)
            #self.device.shell_adb("input tap 450 630")        
            self.device.server.adb.shell("input text 0")
            self.device.delay(1)
            self.device.click(650,1220)
                
            if self.device(resourceId="android:id/button1").exists:
                self.device(resourceId="android:id/button1").click()
            else:
                self.logger.debug("ok is not exists")
                #continue
            if self.device(text="07:00").wait.exists(timeout=2000):
                self.logger.debug("set time is success")
                self.device.delay(180)   
            else:
                self.logger.debug("set time is fail")
                #continue
            for i in range(120):
                self.device.delay(1)
                if self.is_start():
                    break
                if i>=118:
                    self.logger.info("reboot timeout ")
                    return True

