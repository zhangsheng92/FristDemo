# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import logging
import time
import traceback
from datetime import datetime

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not lib_path in sys.path:
    sys.path.append(lib_path)
from automator.uiautomator import Device
from configs import GetConfigs, Configs
from automator.adb import Adb
import random
from configs import AppConfig
from functools import wraps


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result

    return wrapper


class UIParser():
    @staticmethod
    def nest(self, func):
        def wrapper(*args, **kwargs):
            func(args)

        return wrapper

    @staticmethod
    def run(obj, params, exceptfunc=None):
        device = obj if isinstance(obj, Device) else obj.device

        def param_parser(param):
            if isinstance(param, dict):
                for k, v in param.items():
                    if v == None:
                        param.pop(k)
            else:
                for v in param:
                    if v == None:
                        param.remove(v)

        def error(param):
            if param.has_key("assert") and param['assert'] == False:
                return False
            else:
                print "%s error!" % param
                exceptfunc() if (exceptfunc) else None
                return True

        def listfoo(param):
            resault = True
            if isinstance(param["content"], list):
                for content in param["content"]:
                    param_tmp = param
                    param_tmp["content"] = content
                    resault = resault and listfoo(param)
            elif param["id"] == "meta":
                resault = resault and getattr(obj, param["content"])(
                    *param["action"]["param"] if param.has_key("action") and param["action"].has_key("param") else [])
            else:
                print param
                if param_parser(param["id"]) == {}:
                    return True
                select = device(**{param["id"]: param["content"]})
                action = select.wait.exists(timeout=5000) if not param.has_key("wait") else select.wait.exists(
                    timeout=int(param["wait"]))
                if action and not (param.has_key("action") and param["action"] == None):
                    getattr(select, "click")(None) if not param.has_key("action") else getattr(select,
                                                                                               param["action"]["type"])(
                        *param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(
                        param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault

        def dictfoo(param):
            resault = True
            if not param.has_key("id"):
                return False
            if isinstance(param["id"], list):
                for content in param["id"]:
                    param_tmp = param
                    param_tmp["id"] = content
                    if param["id"].has_key("action"):
                        param_tmp["action"] = param["action"]
                    resault = resault and listfoo(param)
            elif param["id"].has_key("meta"):
                resault = resault and getattr(obj, param["id"]["meta"])(
                    *param["action"]["param"] if param.has_key("action") and param["action"].has_key("param") else [])
            else:
                if param_parser(param["id"]) == {}:
                    return True
                select = device(**param["id"])
                # action=select.wait.exists(timeout = 5000) if ((not param.has_key("wait")) or ((param.has_key("wait") and param["wait"]))) else select.wait.exists(timeout = int(param["wait"]))
                action = select.wait.exists(timeout=5000) if not param.has_key("wait") else select.wait.exists(
                    timeout=int(param["wait"]))
                if action and not (param.has_key("action") and param["action"] == None):
                    getattr(select, "click")(None) if not param.has_key("action") else getattr(select,
                                                                                               param["action"]["type"])(
                        *param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(
                        param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault

        for param in params:
            if isinstance(param, list):
                UIParser.run(obj, param)
            else:
                if param.has_key("id") and isinstance(param["id"], dict):
                    if not dictfoo(param):
                        if (error(param)):
                            return False
                elif param.has_key("id") and param.has_key("content") and not isinstance(param["id"], dict):
                    if not listfoo(param):
                        if (error(param)):
                            return False
        return True


def create_folder():
    """Create folder to save pic & log.     
    Return a folder path or None
    Exception: OSError
    """
    log_path = os.environ.get("LOG_PATH")
    if log_path is None:
        log_path = sys.path[0][sys.path[0].find(':') + 1:] + '\\results'
    if not os.path.exists(log_path):
        logger.debug("log_path not exsit")
        os.makedirs(log_path)
    if not os.path.exists(log_path):
        return None
    return log_path


def createlogger(name):
    """Create a logger named specified name with the level set in config file.  
    return a logger
    """
    config = GetConfigs("common")
    lev_key = config.getstr("LOG_FITER", "Default", "common").upper()
    lev_dict = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
                "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL}
    logger = logging.getLogger(name)
    logger.setLevel(lev_dict[lev_key])
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = createlogger("COMMON")


def log_traceback(traceback):
    """print traceback information with the log style.
    """
    str_list = traceback.split("\n")
    for string in str_list:
        logger.warning(string)


def connect_device(device_name):
    """connect_device(device_id) -> Device    
    Connect a device according to device ID.
    """
    environ = os.environ
    device_id = environ.get(device_name)
    if device_id == None:
        device_id = device_name
    backend = Configs("common").get("backend", "Info")
    logger.debug("Device ID is " + device_id + " backend is " + backend)
    if backend.upper() == "MONKEY":
        from automator.monkeyUser import MonkeyUser

        device = globals()["%sUser" % backend](device_id)
    else:
        device = Device(device_id)
    if device is None:
        logger.critical("Cannot connect device.")
        raise RuntimeError("Cannot connect %s device." % device_id)
    return device


def startactivity(serial, packet, activity):
    """start activity
    """
    adb = Adb(serial)
    data = adb.shell("am start -n %s/%s" % (packet, activity))
    if data.find("Error") > -1:
        return False
    return True


def random_name(index_num):
    numseed = "0123456789"
    sa = []
    for i in range(5):
        sa.append(random.choice(numseed))
    stamp = ''.join(sa)
    strname = 'Auto%02d_' % (index_num + 1) + stamp
    logger.debug('Create a random name %s.' % strname)
    return strname


class Common(object):
    """Provide common functions for all scripts."""

    def __init__(self, device, mod, sdevice=None, timeout=5000):
        self.timeout = timeout
        if isinstance(device, Device):
            self.device = device
        else:
            self.device = connect_device(device)
        if sdevice == None:
            pass
        elif isinstance(sdevice, Device):
            self.sdevice = sdevice
        else:
            self.sdevice = connect_device(sdevice)
        self.logger = createlogger(mod)
        self.log_path = create_folder()
        self.config = GetConfigs("common")
        self.appconfig = AppConfig("appinfo")
        self.appconfig.set_section(mod)
        self.adb = self.device.server.adb
        self.suc_times = 0
        if device == "MDEVICE":
            self.mdevice_tel, self.mdevice_msg = number_tel(os.environ.get(device))
        elif not isinstance(device, Device):
            self.mdevice_tel, self.mdevice_msg = number_tel(device)
        if sdevice != None:
            if sdevice == "SDEVICE":
                self.sdevice_tel, self.sdevice_msg = number_tel(os.environ.get(sdevice))
            elif not isinstance(sdevice, Device):
                self.sdevice_tel, self.sdevice_msg = number_tel(sdevice)
        try:
            self.mod_cfg = GetConfigs(mod)
            self.test_times = 0
            self.dicttesttimes = self.mod_cfg.get_test_times()
            for test_time in self.dicttesttimes:
                self.test_times += int(self.dicttesttimes[test_time])
            self.logger.info("Trace Total Times " + str(self.test_times))
        except:
            pass

    def device(self):
        return self.device

    def sdevice(self):
        return self.sdevice

    def save_fail_img(self, newimg=None):
        """save fail image to log path.        
        argv: The picture want to save as failed image.
        """
        path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        if newimg is None:
            self.logger.debug("Take snapshot.")
            newimg = self.device.screenshot(path)
        if newimg is None:
            self.logger.warning("newimg is None.")
            return False
        self.logger.error("Fail: %s" % (path))
        return True

    def save_fail_img_s(self, newimg=None):
        """save fail image to log path.
        argv: The picture want to save as failed image.
        """
        path = (self.log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        if newimg is None:
            self.logger.debug("s-device Take snapshot.")
            newimg = self.sdevice.screenshot(path)
        if newimg is None:
            self.logger.warning("newimg is None.")
            return False
        self.logger.error("Fail: %s" % (path))
        return True

    def get_file_num(self, path, format):
        """get number of file with specified format.
        """
        content = self.adb.shell("ls " + path)
        num = content.count(format)
        self.logger.debug("%s file num is %d." % (format, num))
        return num

    def start_activity(self, packet, activity):
        data = self.device.server.adb.shell("am start -n %s/%s" % (packet, activity))
        if data.find("Error") > -1:
            self.logger.error("Fail: %s/%s" % (packet, activity))
            return False
        return True

    def start_app(self, name, b_desk=True):
        """start app
        arg: name(str) app name
             b_desk(Boolean) whether to start on the desktop
        """
        self.logger.debug("start app:%s" % name)
        #self.device.server.adb.restart_viewserver()
        if b_desk and self.device(text=name).exists:
            self.device(text=name).click()
            return True
        self.device.press.home()
        if b_desk and self.device(text=name).wait.exists(timeout=2000):
            self.device(text=name).click()
            return True
        elif b_desk and self.device(description=name).exists:
            self.device(description=name).click()
            return True
        elif self.device(description="Apps").wait.exists(timeout=2000):
            self.device(description="Apps").click()
            if self.device(text=name).wait.exists(timeout=2000):
                self.device(text=name).click()
                return True
            self.device(scrollable=True, resourceId="com.tct.launcher:id/apps_list_view").scroll.vert.toBeginning()
            self.device(scrollable=True).scroll.vert.to(text=name)
            self.device(text=name).click()
            return True
        return False

    def back_to_all_apps(self):
        """back_to_all_apps.
        """
        # self.logger.debug("back to all apps")
        for loop in range(4):
            self.device.press.back()
            if self.device(text="exit").wait.exists(timeout=500):
                self.device(text="exit").click()
            elif self.device(text="Quit").wait.exists(timeout=500):
                self.device(text="Quit").click()
            if self.device(resourceId=self.appconfig.id("id_group_title", "MenuNavigation")).wait.exists(timeout=500):
                return True

    def start_all_app(self, num=3):
        '''Call/People/ALL APPS/Messaging/Browser'''
        self.logger.debug("start all app")
        if self.device(description="ALL APPS").exists:
            self.device(description="ALL APPS").click()
        elif self.device(description="Apps").exists:
            self.device(description="Apps").click()
            self.device().fling.horiz.toBeginning()
        self.device().fling.horiz.toBeginning()
        for loop in range(3):
            self.adb.shell("input swipe 500 350 500 1600")
        for i in range(num):
            for j in range(self.device(className="android.widget.TextView").count - 2):
                if self.device(resourceId="com.tct.launcher:id/apps_customize_pane_content").child(index=0).child(
                        index=i).exists:
                    self.device(resourceId="com.tct.launcher:id/apps_customize_pane_content").child(index=0).child(
                        index=i).child(index=j).click()
                    self.device(text="ALL APPS").wait.gone(timeout=20000)
                    self.back_to_all_apps()
            self.device().fling.horiz.forward()
        return False

    def select_menu_item(self, stritem):
        self.device.press.menu()
        self.device.delay(1)
        self.device(text=stritem).click()
        self.device.delay(2)

    def _is_connected(self, type):
        temp_type = type
        if type == "ALL":
            temp_type = "LTE"
        for i in range(5):
            if self.adb.get_data_service_state() == temp_type:
                break
            self.device.delay(5)
        else:
            self.logger.warning("Cannot get %s service." % (type))
            self.device.press.back()
            return False
        for i in range(5):
            if self.adb.get_data_connected_status():
                return True
            self.device.delay(5)
        else:
            self.logger.warning("Cannot connect %s data." % (type))
            self.device.press.back()
            return False

    def switch_network(self, type=None):
        """switch network to specified type.    
        argv: (str)type -- the type of network.    
        """
        self.logger.debug("Switch network to %s." % (type))
        self.start_activity(self.appconfig("RadioInfo", "package"), self.appconfig("RadioInfo", "activity"))
        self.device.delay(2)
        network_type = self.appconfig("RadioInfo", type)
        self.device(scrollable=True).scroll.to(text=self.appconfig("RadioInfo", "set"))
        if self.device(resourceId=self.appconfig.id("RadioInfo", "id_network")).wait.exists(timeout=2000):
            self.device(resourceId=self.appconfig.id("RadioInfo", "id_network")).click()
        self.device(scrollable=True).scroll.to(text=network_type)
        self.device.delay(1)
        self.device(text=network_type).click()
        self._is_connected(type)
        self.back_to_home()
        

    def back_to_home(self):
        """back_to_home.
        """
        for loop in range(4):
            self.device.press.back()
            self.device.delay(1)
        # self.device.swipe(1350,1980,50,1980, 10)
        self.device.delay(1)
        #self.device.server.adb.shell("am start -n com.android.settings/com.android.settings.Settings")
        #self.device.delay(1)
        self.device.press.home()

    def back_to_home_s(self):
        """back_to_home.
        """
        for loop in range(4):
            self.sdevice.press.back()
            self.sdevice.delay(1)
        self.sdevice.press.home()

    def is_playing_video(self):
        """check if video is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media.player")
        if not data:
            return None
        if "Client" in data:
            self.logger.debug("The video is playing now")
            return True
        else:
            self.logger.debug("The video is not playing.")
            return False

    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False

    def clear_notification(self):
        self.logger.info("clear notification")
        if self.device(description="Clear all notifications.").exists:
            self.device(description="Clear all notifications.").click()
            return True
        self.device.open.notification()
        if self.device(description="Clear all notifications.").wait.exists(timeout=2000):
            self.device(description="Clear all notifications.").click()
            self.device.delay(1)
            return True
        elif self.device(scrollable=True).exists:
            self.device.swipe(500, 1200, 500, 800)
            if self.device(description="Clear all notifications.").wait.exists(timeout=2000):
                self.device(description="Clear all notifications.").click()
                self.device.delay(1)
                return True
        self.device.press.back()

    def exception_end_call(self):
        """when exception happened, m-device end the call
        """
        self.device.press.home()
        self.start_app(self.appconfig("name", "Dialer"))
        self.device.delay(2)
        if self.device(text="Return to call in progress").exists:
            self.logger.debug("Exception end call")
            self.device.delay(1)
            self.device(text="Return to call in progress").click()
            if self.device(description="End").wait.exists(timeout=self.timeout):
                self.device(description="End").click()
                self.device.delay(2)
                self.device.press.home()
        self.device.press.home()

    def random_name(self, index_num):
        numseed = "0123456789"
        sa = []
        for i in range(5):
            sa.append(random.choice(numseed))
        stamp = ''.join(sa)
        strname = 'Auto%02d_' % (index_num + 1) + stamp
        logger.debug('Create a random name %s.' % strname)
        return strname

    def clear_background(self):
        self.logger.info("clear the background")
        self.device.press.recent()
        if self.device(description="Clear all").wait.exists(timeout=2000):
            self.device(description="Clear all").click()
        else:
            self.device.click(725, 2140)
        self.device.press.home()

    def charging_full(self, critical=20):
        if int(self.adb.shell("cat sys/class/power_supply/battery/capacity")) < critical:
            self.logger.info("battery is less than %s, start charging to full" % critical)
            self.device.sleep()
            while True:
                if int(self.adb.shell("cat sys/class/power_supply/battery/capacity")) == 100:
                    self.logger.info("battery is full")
                    self.device.wakeup()
                    self.device.delay(1)
                    self.device.swipe(720, 2000, 807, 600, 50)
                    return True
                else:
                    self.device.delay(600)


def number_tel(device):
    number = {
        "OJIRIVLZ99PZIZRS": ["13255226220", "13255226220"],  # Team1
        "f69ce4a": ["13003323342", "13003323342"],  # Team2
        "0123456789ABCDEF": ["661360", "18658271360"],  # Team3
        "BMLZRGP7S8F6LBY9": ["13236439881", "13236439881"],  # Team4
        "9HLJD6MVKJMVDUPR": ["13003327358", "13003327358"],  #Team5
        "8eec23f1": ["665443", "18667825443"],  #Team6

        "0123456789ABCDEF": ["13003323342", "13003323342"],  #T1
        "2cd8f42c": ["666721", "18658236721"],  #T2
        "2cd0f034": ["661930", "18658231930"],  #T3
        "2c9cdc2c": ["660862", "18658230862"],  #T4
        "2cc8e62b": ["667612", "18657437612"],  #T5
        "2cd0e633": ["668713", "18658238713"],  #T6

        "be3ddf58": ["661930", "18658231930"],
        "49a9b1f2": ["666721", "18658236721"],

        "be39db55": ["665783", "18667885783"],
        "4997e36c": ["665443", "18667825443"],

        "49b9a1f8": ["666275", "18668586275"],
        "be39ef55": ["663230", "18658273230"],

        "be51f559": ["660862", "18658230862"],
        "49e1a1ed": ["660653", "18658470653"],

        "be59e955": ["668713", "18658238713"],
        "49efe16c": ["667612", "18657437612"]

    }
    if number.has_key(device):
        return number[device]
    else:
        logger.warning("%s device not number exists" % device)
        return None, None


#if __name__ == "__main__":
    #a = Common("80c08ac6", "Common")
    #a.start_app("Contacts")
