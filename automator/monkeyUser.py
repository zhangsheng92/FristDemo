# -*- coding: UTF-8 -*-

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.monkeyrunner import MonkeyImage
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By

from interface import IDevice,MetaInterfaceChecker
from atomic import *
from lang import Lang
from datetime import datetime

from base import *

MDAU = MonkeyDevice.DOWN_AND_UP

logger = createlogger("COMMON")


class UiObject(object):

    '''Represent a UiObject, on which user can perform actions, such as click, set text
    
    TO DO!!
    '''

    __alias = {'description': "contentDescription"}

    def __init__(self, device, selector):
        pass


class MonkeyUser(object):
    # the interface
    __metaclass__ = MetaInterfaceChecker
    __implements__ = (IDevice, ) # 必须实现的接口
    
    def __init__(self, device,log_name):
        environ = os.environ
        self.device_id = environ.get(device)
        if (self.device_id == None):
            device_id = device
        self._device,self._easy_device,self.hierarchyviewer = self._connect_device(self.device_id)
        self._logger = createlogger(log_name)
        self._log_path = create_folder()
        self._config = GetConfigs("common")
        self._lang = Lang(device_id)

    def _connect_device(self,device, is_restart=False):
        """connect_device(device_id) -> MonkeyDevice
        
        Connect a device according to device ID.
        argv: (boolean)is_restart -- whether need restart view server before connect
        author:Zhihao.Gu
        """
        logger.debug("Device ID is " + device)
        device = MonkeyRunner.waitForConnection(5,device)
        if device is None:
            logger.critical("Cannot connect device.")
            raise RuntimeError("Cannot connect %s device." % device)
        if is_restart:
            self._restart_viewserver(device)
        easy_device = EasyMonkeyDevice(device)
        hierarchyviewer = device.getHierarchyViewer()
        return (device,easy_device,hierarchyviewer)


    @property
    def info(self):
        '''Get the device info.'''
        pass

    def click(self, x, y):
        '''click at arbitrary coordinates.'''
        return self._device.touch(x,y,MDAU)

    def long_click(self, x, y):
        '''long click at arbitrary coordinates.'''
        return self._device.touch(x,y,MDAU)

    def swipe(self, sx, sy, ex, ey, steps=100):
        self._device.shell("input swipe %s %s %s %s"%(sx, sy, ex, ey))

    def drag(self, sx, sy, ex, ey, steps=100):
        '''Swipe from one point to another point.'''
        self._device.drag((sx,sy),(ex,ey),0.1,steps)

    def screenshot(self, filename, scale=1.0, quality=100):
        '''take screenshot.'''
        device_file = self.server.jsonrpc.takeScreenshot("screenshot.png",
                                                         scale, quality)
        if not device_file:
            return None
        p = self.server.adb.cmd("pull", device_file, filename)
        p.wait()
        self.server.adb.cmd("shell", "rm", device_file).wait()
        return filename if p.returncode is 0 else None

    @property
    def press(self):
        '''
        press key via name or key code. Supported key name includes:
        home, back, left, right, up, down, center, menu, search, enter,
        delete(or del), recent(recent apps), volume_up, volume_down,
        volume_mute, camera, power.
        Usage:
        d.press.back()  # press back key
        d.press.menu()  # press home key
        d.press(89)     # press keycode
        '''
        @param_to_property(
            key=["home", "back", "left", "right", "up", "down", "center",
                 "menu", "search", "enter", "delete", "del", "recent",
                 "volume_up", "volume_down", "volume_mute", "camera", "power"]
        )
        def _press(key, meta=None):
            if isinstance(key, int):
                print "int %s"%key
            else:   
                self._device.press('KEYCODE_%s'%key.upper(), MonkeyDevice.DOWN_AND_UP)
            return True   
        return _press


    def _is_screen_on(self):     
        if is_screen_on(self.device_id):
            logger.debug("The screen is on now")
            return True
        else:
            logger.debug("The screen is off now")
            return False  

    def wakeup(self):
        """This method simulates pressing the power button if the screen is OFF 
        else it does nothing if the screen is already ON."""
        if self._is_screen_on():
            return False
        else:        
            self.press.power()
            return True

    def sleep(self):
        '''turn off screen in case of screen on.'''
        pass
    
    @property
    def screen(self):
        '''
        Turn on/off screen.
        Usage:
        d.screen.on()
        d.screen.off()
        '''
        @param_to_property(action=["on", "off"])
        def _screen(action):
            return self.wakeup() if action == "on" else self.sleep()
        return _screen

#     def unlock_screen(self):
#         """unlock screen(slide)
#         author:Guowei.zhang
#         """
#         self._device.press("KEYCODE_POWER", MDAU)
#         MonkeyRunner.sleep(1)
#         self._device.wake()
#         MonkeyRunner.sleep(3)
#         self._device.drag((260, 650),(260, 930), 0.5,3)
#         MonkeyRunner.sleep(1)
#         if self._easy_device.getFocusedWindowId() !=  'Keyguard':
#             return True
#         else:
#             return False

    def wait_for_exists(self,node_id,step,times):
        """Waits a specified length of steps&times for a UI element or packetage to become visible."""
        maxTime = 0
        if str(node_id).find("id"): 
            while (not self._easy_device.visible(By.id(node_id))) and maxTime <= times:
                maxTime = maxTime + 1
                self._logger.debug("Wait for skip...")
                MonkeyRunner.sleep(step)
            if maxTime > times:
                self._logger.warning("can't enter the designated page")
                return False
            else :
                self._logger.debug("Enter designated Page Successfully")
                return True          
        else:
            pass
        


    def wait_until_gone(self,node_id,step,times):
        "Waits a specified length of time for a UI element to become undetectable."
        return True

    @property
    def wait(self):
        '''
        Waits for the current application to idle or window changed.
        Usage:
        d.wait.idle(timeout=1000)
        d.wait.update(timeout=1000, package_name="com.android.settings")
        '''
        @param_to_property(action=["idle", "update"])
        def _wait(action, timeout=1000, package_name=None):
            if action == "idle":
                return self.wait_until_gone()
            elif action == "update":
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForWindowUpdate(package_name, timeout)
        return _wait


    def exists(self, **kwargs):
        '''Check if the specified ui object by kwargs exists.'''
        return self(**kwargs).exists

    def get_current_activity(self):
        return self._easy_device.getFocusedWindowId()
    
    def get_current_package(self):
        pass 


    def translate(self, lang_id):
        """get string from language.initActions
        
        argv: (str)lang_id -- option name in file
        author: Zhihao.Gu 
        """
        value = self._lang.translate(lang_id)
        self._logger.debug("Translate %s to %s." % (lang_id, value))
        return value


    def is_access_network(self):
        """check if it access the network or not.
        
        author: Leping.Zheng
        """ 
        return get_data_service_state(self.device_id)       
        
        
    def get_data_service_state(self):
        """get data service state to judge whether attach the operator network.
        """
        return get_data_service_state(self.device_id)

        
    def switch_network(self,type = None):
        """switch network to specified type.
        
        argv: (str)type -- the type of network.
        author: Leping.Zheng        
        """
        self._logger.debug("Switch network to %s." % (type))
        if not self.start_app("com.android.settings/com.android.settings.RadioInfo"):
            self._logger.warning("Cannot launch activity to switch network.")
            return False
        if not type in ('2G','3G','LTE','All'):
            self._device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP)
            self._logger.warning("Wrong argument: %s." % (type))
            return False
        if type == '2G':
            text_type = 'GSM only'
        elif type == '3G':
            text_type = 'WCDMA only'
        elif type == 'LTE':
            text_type = 'LTE only'
        elif type == 'All':
            text_type = 'LTE/GSM/CDMA auto (PRL)'
        smsc_node = self.get_node('id/smsc')
        if smsc_node is None:
            self._logger.warning("Cannot find node 'id/smsc'.")
            raise TypeError("Cannot get node 'id/smsc'.")
        if smsc_node.namedProperties.get('isFocused').value == 'true':
            self._logger.debug("Exist input method.")
            self._device.press("KEYCODE_BACK", MDAU)
            MonkeyRunner.sleep(1)
        self._device.drag((400,700),(400,100),0.1,10)
        MonkeyRunner.sleep(1)
        self._device.drag((400,700),(400,100),0.1,10)
        MonkeyRunner.sleep(1)
        netmode_node = self.get_node('id/text1')
        if netmode_node is None:
            self._device.press("KEYCODE_BACK",MonkeyDevice.DOWN_AND_UP)
            self._logger.warning("Cannot find node 'id/text1'.")
            raise TypeError("Cannot get node 'id/text1'.")
        netmode_text = self._hierarchyviewer.getText(netmode_node)
        netmodepos = self._hierarchyviewer.getAbsoluteCenterOfView(netmode_node)
        if text_type not in netmode_text:
            self._device.touch(netmodepos.x,netmodepos.y,MonkeyDevice.DOWN_AND_UP)
            MonkeyRunner.sleep(2)
            self._device.drag((400,400),(400,1000),0.1,10)
            self._device.drag((400,400),(400,1000),0.1,10)
            MonkeyRunner.sleep(1)
            if text_type == 'GSM only' or text_type == 'WCDMA only':
                pass
            else:
                self._device.drag((400,900),(400,400),0.5, 4)
                MonkeyRunner.sleep(1)
            self._easy_device.touchtext(By.id("id/text1"),text_type,MonkeyDevice.DOWN_AND_UP)
            MonkeyRunner.sleep(3)
            j = 0
            if type == 'All':
                config = GetConfigs("common")
                support = config.getstr("Default","NETWORK_TYPE","common")
                if "LTE" in support:
                    type = "LTE"
                else:
                    type = "3G"
            while self.get_data_service_state() != type and j < 5:
                MonkeyRunner.sleep(4)
                j += 1
            if j == 5:
                self._logger.warning("Cannot get %s service." % (type))
                self._device.press("KEYCODE_BACK",MonkeyDevice.DOWN_AND_UP)
                return False
            else:
                max_time = 0
                while not self.get_data_connected_status():
                    MonkeyRunner.sleep(4)
                    max_time += 1
                    if (max_time) > 10:
                        self._logger.warning("Cannot connect %s data." % (type))
                        self._device.press("KEYCODE_BACK",MonkeyDevice.DOWN_AND_UP)
                        return False
        self._logger.debug("Switch network to %s." % (type))
        self._device.press("KEYCODE_BACK",MonkeyDevice.DOWN_AND_UP)
        return True


    def check_winid(self, win_id):
        """check window id whether same as the specified.
        
        argv: (tuple)win_id -- list of window ids.
        author: Zhihao.Gu
        """
        if type(win_id) is str:
            win_id = (win_id,)
        for item in win_id:
            if item == self.get_current_activity():
                return True
        return False
      
    def is_enter_app(self, win_id,step,times):
        """check whether enter the specified activity.
        """
        self._logger.debug("Check if enter specified app.")
        if type(win_id) is str:
            win_id = (win_id,)
        counter = 0
        self._logger.debug("Check current window ID.")
        while not self.check_winid(win_id):
            MonkeyRunner.sleep(step)
            counter += 1
            if (counter) == times:
                cwinID = self.get_current_activity()
                if cwinID is not None:
                    self._logger.warning("Current Win ID is %s." %(cwinID))
                return False
        return True

    def start_app(self, app_id, *win_id):
        """Launch application by 'startActivity'.
        
        function check whether in the application before launch.
        argv: (str)app_id -- launch id
              (str)win_id -- id of displayed window
        author: Zhihao.Gu
        """
        self._logger.debug("Start %s." %(app_id))
        if len(win_id) == 0:
            win_id = (app_id,)
        if self.check_winid(win_id):
            return True
        self._device.startActivity(app_id)
        MonkeyRunner.sleep(1)
        if self.is_enter_app(win_id):
            return True
        else:
            MonkeyRunner.sleep(2)
            if self.is_enter_app(win_id):
                return True
        self._logger.warning("Can not start %s." %(app_id))
        return False

    def get_node(self, strID, root_node = None, flag = True):
        """searching specified node by object id start from root node.
        
        argv: (str)strID -- object id of node.
              (node)root_node -- the root node begin searching. If root_node is 
              none, search all node.
              (boolean)flag -- whether restart viewserver.
        """
        tempnode = None
        Maxtime = 0
        while tempnode is None:
            Maxtime = Maxtime + 1
            if flag and Maxtime == 2:
                self._logger.warning("Get node fail, restart viewserver!")
                restart_viewserver(self._device)
            if Maxtime > 3:
                return None
            if root_node is None:
                tempnode = self._hierarchyviewer.findViewById(strID)
            else:
                tempnode = self._hierarchyviewer.findViewById(strID,root_node)
            MonkeyRunner.sleep(1)
        return tempnode

    def save_fail_img(self, newimg = None):
        """save fail image to log path.
        
        argv: (MonkeyImage)newimg -- The picture want to save as failed image.
        author: Zhihao.Gu
        """
        if newimg is None:
            self._logger.debug("Take snapshot.")
            newimg = self._device.takeSnapshot()
        if newimg is None:
            self._logger.warning("newimg is None.")
            return False
        path = (self._log_path + "\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        newimg.writeToFile(path, 'png')
        self._logger.error("Fail: %s" %(path))
        return True
         
    def select_menu(self, item,id = "id/title"):
        """select menu option.
        
        argv: (str)item -- option display in menu list.
        return void
        author: Zhihao.Gu
        """
        self._logger.debug("Select menu option: %s." % item)
        self._device.press("KEYCODE_MENU", MDAU)
        MonkeyRunner.sleep(1)
        self._easy_device.touchtext(By.id(id), item, MDAU)
        MonkeyRunner.sleep(1)
        
   
    def back_to_home(self):
        """check if the screen is on or not"""
        self._logger.debug("Back to home screen.")
        for backtimes in range(6):
            self._device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
            MonkeyRunner.sleep(0.2)
        self._device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(1)
        
    def is_lte(self,step = 2,times = 10):
        '''check if it stays at lte network or not.

        author:Leping.Zheng
        '''
        i = 0
        # Try to wait for 20 sec at most if state is unknown
        while get_data_service_state() != 'LTE' and i < times:
            time.sleep(step)
            i += 1
        if i < times:
            self._logger.debug("Change to LTE.")
            return True
        else:
            self._logger.warning("Cannot change to LTE")
            return False
        

       
if __name__ == '__main__':
    pass