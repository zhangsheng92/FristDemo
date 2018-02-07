# -*- coding: UTF-8 -*-

import os
import re
import subprocess
import time
# from common.simcard import *
import smtplib
from email.mime.text import MIMEText

mail_host = "mail.tcl.com"
mail_user = "atttest02@tcl.com"
mail_pass = "StabilityTest02"

def send_mail_exception(To,device):
     
        msg = MIMEText( 'zxcvbnm', _subtype="plain", _charset="utf-8")
        msg["Subject"] = "%s device not connected"%device
        msg["From"] = mail_user
        msg["To"] = To
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(mail_user, To, msg.as_string())
            server.close()
            return True
        except Exception, e:
            return False   

class Adb(object):

    def __init__(self, serial=None, adb_server_host=None, adb_server_port=None):
        self.__adb_cmd = None
        self.default_serial = serial if serial else os.environ.get("ANDROID_SERIAL", None)
        self.adb_server_host = str(adb_server_host if adb_server_host else 'localhost')
        self.adb_server_port = str(adb_server_port if adb_server_port else '5037')
        self.adbHostPortOptions = []
        if self.adb_server_host not in ['localhost', '127.0.0.1']:
            self.adbHostPortOptions += ["-H", self.adb_server_host]
        if self.adb_server_port != '5037':
            self.adbHostPortOptions += ["-P", self.adb_server_port]

    def adb(self):
        if self.__adb_cmd is None:
            if "ANDROID_HOME" in os.environ:
                filename = "adb.exe" if os.name == 'nt' else "adb"
                adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", filename)
                if not os.path.exists(adb_cmd):
                    raise EnvironmentError(
                        "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
            else:
                import distutils
                if "spawn" not in dir(distutils):
                    import distutils.spawn
                adb_cmd = distutils.spawn.find_executable("adb")
                if adb_cmd:
                    adb_cmd = os.path.realpath(adb_cmd)
                else:
                    raise EnvironmentError("$ANDROID_HOME environment not set.")
            self.__adb_cmd = adb_cmd
        return self.__adb_cmd

    def cmd(self, *args, **kwargs):
        '''adb command, add -s serial by default. return the subprocess.Popen object.'''
        serial = self.device_serial()
        if serial:
            if " " in serial:  # TODO how to include special chars on command line
                serial = "'%s'" % serial
            return self.raw_cmd(*["-s", serial] + list(args))
        else:
            return self.raw_cmd(*args)

    def raw_cmd(self, *args):
        '''adb command. return the subprocess.Popen object.'''
        cmd_line = [self.adb()] + self.adbHostPortOptions + list(args)
        if os.name != "nt":
            cmd_line = [" ".join(cmd_line)]
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def device_serial(self):
        if not self.default_serial:
            devices = self.devices()
            if devices:
                if len(devices) is 1:
                    self.default_serial = list(devices.keys())[0]
                else:
                    raise EnvironmentError("Multiple devices attached but default android serial not set.")
            else:
                raise EnvironmentError("Device not attached.")
        return self.default_serial

    def devices(self):
        '''get a dict of attached devices. key is the device serial, value is device name.'''
        out = self.raw_cmd("devices").communicate()[0].decode("utf-8")
        match = "List of devices attached"
        index = out.find(match)
        if index < 0:
            raise EnvironmentError("adb is not working.")
        return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

    def forward(self, local_port, device_port):
        '''adb port forward. return 0 if success, else non-zero.'''
        return self.cmd("forward", "tcp:%d" % local_port, "tcp:%d" % device_port).wait()

    def forward_list(self):
        '''adb forward --list'''
        version = self.version()
        if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
            raise EnvironmentError("Low adb version.")
        lines = self.raw_cmd("forward", "--list").communicate()[0].decode("utf-8").strip().splitlines()
        return [line.strip().split() for line in lines]

    def version(self):
        '''adb version'''
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.raw_cmd("version").communicate()[0].decode("utf-8"))
        return [match.group(i) for i in range(4)]

    def shell(self, *args):
        '''adb command. return the shell value'''
        serial = self.device_serial()
        if serial.find(" ") > 0:  # TODO how to include special chars on command line
            serial = "'%s'" % serial
        cmd_line = ["-s", serial,"shell"] + list(args)
        if self.adb_server_port:  # add -P argument
            cmd_line = ["-P", str(self.adb_server_port)] + cmd_line
        if self.adb_server_host:  # add -H argument
            cmd_line = ["-H", self.adb_server_host] + cmd_line
        cmd_line = ['"%s"'%self.adb()]+cmd_line
        #print cmd_line
        return os.popen(" ".join(cmd_line)).read()
    
    
    def get_device_seriono(self):
        '''
        get device serial
        Usages:
        d.get_device_seriono()
        '''
        return self.shell("getprop ro.serialno").strip()
    
    
    def get_device_name(self):
        '''
        get Build.product name
        Usages:
        d.get_device_name()
        '''
        return self.shell("getprop ro.build.product").strip()

    def get_device_version(self):
        '''
        get product version
        Usages:
        d.get_device_version()
        '''
        return self.shell("getprop ro.build.version.incremental").strip()   
    
    def get_device_manufacturer(self):
        '''
        Get manufacturer Info
        Usages:
        d.get_device_manufacturer()
        '''
        return self.shell("getprop ro.product.manufacturer").strip()
    
    def get_device_brand(self):
        '''
        Get brand Info
        Usages:
        d.get_device_brand()
        '''
        return self.shell("getprop def.tctfw.brandMode.name").strip()
    
    def get_device_model(self):
        '''
        Get Build.MODEL Info
        Usages:
        d.get_device_model()
        '''
        return self.shell("getprop ro.product.model").strip()

    def get_current_lang(self):
        '''
        Get language Info
        Usages:
        d.get_current_lang()
        '''       
        return self.shell("getprop persist.sys.language").strip()
 
    def get_cpuinfo(self):
        '''
        Get cpu Info
        Usages:
        d.get_current_lang()
        '''      
        return self.shell("getprop ro.product.cpu.abi").strip()
    
    def call(self,phone):
        '''
        call number
        Usages:
        d.call("10010")      
        '''
        data = self.shell("am start -a android.intent.action.CALL -d tel:%s"%(phone))
        return True
    
    def get_call_state(self):
        return True
    
    def send_sms(self,phonenum,smsbody):
        '''
        send sms
        Usages:
        d.send_sms("10010","abcdefg")      
        '''
        data = self.shell("am start -a android.intent.action.SENDTO -d sms:%s --es %s cxye"%(phonenum,smsbody))
        self.shell("adb shell input keyevent 22")
        self.shell("adb shell input keyevent 66")
        return True
    
    def get_meminfo(self):
        return True

    def get_current_packagename(self):
        return True
    
    def get_data_connected_status(self):
        ''''get the status of data connection.
        Usages:
        d.get_data_connected_status()      
        '''
        status = self.shell("dumpsys telephony.registry")
        if "mDataConnectionState=2" in status:
            return True
        return False

    def get_data_service_state(self):          
        '''get data service state to judge whether attach the operator network.
        Usages:
        d.get_data_service_state()  
        '''
        print("Check data service status.") 
        data = self.shell("dumpsys telephony.registry")
        if not data:
            return None    
        index = data.find("mServiceState")
        if index < 0:           
            return None
        index2 = data.find("\n", index)
        assert index2 > 0        
        data = data[index:index2-1].lower()
        if (data.find("edge") > 0 or data.find ("gprs") > 0 or 
            data.find("1xrtt") > 0):
            return "2G"
        elif (data.find("evdo") > 0 or data.find("hsupa") > 0 or 
              data.find("hsdpa") > 0 or data.find("hspa") > 0):
            return "3G"
        elif data.find("lte") > 0:
            return "LTE"            
        else: 
            return "UNKNOWN"  


    def is_access_network(self):
        '''check if it access the network or not.
        Usages:
        d.get_data_service_state()  
        '''
        data = self.shell("dumpsys telephony.registry")
        if not data:
            return False
        if data.find("mServiceState=0") > -1:
            print("Access the network .")
            return True
        else:
            print("Cannot access the network ")
            return False
    
    def restart_viewserver(self):
        '''restart viewserver if it no respon
        Usages:
        d.restart_viewserver()  
        '''
        self.shell("dumpsys telephony.registry")
        self.shell("service call window 2")
        time.sleep(2)
        result = self.shell("service call window 3")
        if result.find("00000000 00000000") > -1:
            self.shell("service call window 1 i32 4939")
            time.sleep(2)
            result = self.shell("service call window 3")
            if result.find("00000000 00000001") > -1:
                return True
            else:
                print("Start viewserver fail.")
                return False
        else:
            print("Exit viewserver fail.")
            return False 
 
    def is_screen_on(self):
        '''check if the screen is on or not
        Usages:
        d.is_screen_on()  
        '''
        data = self.shell("dumpsys display")
        if data:
            return None
        if data.find("mBlanked=false")>-1:
            return True
        else:
            return False

    def get_file_num(self,path,format):
        '''get number of file with specified format.
        Usages:
        d.is_screen_on()  
        '''
        content = self.shell("ls " + path)
        num = content.count(format)
    #     self._logger.debug("%s file num is %d." % (format,num))
        return num


    def startactivity(self,packet,activity):
        '''start activity by shell
        Usages:
        d.is_screen_on()  
        '''
        data = self.shell("am start -n %s/%s"%(packet,activity))
        if data.find("Error")>-1:
            return False
        return True
 
if __name__ == "__main__":
    a = Adb("a6eac273")
    print a.get_device_name()
    print a.get_device_version()
    print a.get_device_seriono()
    print a.get_device_manufacturer()
        
    print a.get_device_model()
    print a.get_current_lang()

    print a.get_cpuinfo()

    