# -*- coding: UTF-8 -*-
"""Settings library for scripts.
"""

from common import Common, UIParser
from chrome import Chrome
#from browser import Browser


class Settings(Common):
    """Provide common functions involved wifi,display,sound etc."""

    def enter_settings(self, option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug(option)
        self.start_app("Settings")
        if self.device(text=self.appconfig("settings", "Settings")).wait.exists(timeout=2000):
            self.logger.debug("enter Settings")
            if self.device(text=option).exists:
                self.device(text=option).click()
            else:
                self.device(scrollable=True).scroll.vert.to(text=option)
                if self.device(text=option).wait.exists(timeout=10000):
                    self.device(text=option).click()
                else:
                    return False
            if self.device(text=self.appconfig("settings", "Settings")).wait.gone(timeout=2000):
                self.logger.debug("enter " + option + " setting")
                return True
        return False
        
    def enter_settings_s(self, option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug(option)
        self.sdevice.press.home()
        self.sdevice(description="Apps").click()
        if self.sdevice(text="Settings").wait.exists(timeout=2000):
            self.sdevice(text="Settings").click()
            if self.sdevice(text=self.appconfig("settings", "Settings")).wait.exists(timeout=2000):
                self.logger.debug("enter Settings")
            else :
                self.logger.debug("cannot enter Settings")
                return False
        else :     
            self.sdevice(scrollable=True, resourceId="com.tct.launcher:id/apps_list_view").scroll.vert.toBeginning()
            self.sdevice(scrollable=True).scroll.vert.to(text="Settings")
            self.sdevice(text="Settings").click()
            self.sdevice.delay(1)
            if self.sdevice(text=self.appconfig("settings", "Settings")).wait.exists(timeout=2000):
                self.logger.debug("enter Settings")
            else :
                self.logger.debug("cannot enter Settings")
                return False
        if self.sdevice(text=option).exists:
            self.sdevice(text=option).click()
        else:
            self.sdevice(scrollable=True).scroll.vert.to(text=option)
            if self.sdevice(text=option).wait.exists(timeout=10000):
                self.sdevice(text=option).click()
            else:
                return False
        if self.sdevice(text=self.appconfig("settings", "Settings")).wait.gone(timeout=2000):
            self.logger.debug("enter " + option + " setting")
            return True

    '''def switch_network(self, type=""):
        """switch network to specified type.
        argv: (str)type -- the type of network.
        """
        network_type = self.appconfig(type, "Settings")
        self.logger.debug("Switch network to %s:%s." % (type, network_type))
        if self.enter_settings("More"):
            if self.device(text="Cellular networks").wait.exists(timeout=1000):
                self.device(text="Cellular networks").click()
            elif self.device(text="Mobile networks").wait.exists(timeout=1000):
                self.device(text="Mobile networks").click()
            connect = [
                #{"id": {"text": self.appconfig("networks", "Settings")}},
                {"id": {"text": "Preferred network type"}},
                {"id": {"text": network_type}},
            ]
            if not UIParser.run(self, connect):
                self.save_fail_img()
                return False
        print self._is_connected(type)
        self.back_to_home()'''

    def switch_network(self , type = None) :
        """switch network to specified type.
        argv: (str)type -- the type of network.
        """
        self.logger.debug("Switch network to %s." % (type))
        self.enter_settings("Mobile Networks")
        self.device(text = "Network operators").click.wait(timeout = 1000)
        if self.device(textContains = type).wait.exists(timeout = 50000) :
            self.device(textContains = type).click.wait(timeout = 1000)
            self.logger.debug("Switch network %s success." % (type))
            self.back_to_home()


class Wifi(Settings):
    def __init__(self, device, log_name, sdevice=None):
        Settings.__init__(self, device, log_name, sdevice)
        self.chrome = Chrome(self.device, "wifi_chrome")
        #self.browser = Browser(self.device, "wifi_browser")

    def enter(self):
        '''enter wifi settings
        '''
        return self.enter_settings(self.appconfig("wifi", "Settings"))

    def back_to_wifi(self):
        '''back to wifi list
         argv:
        '''
        self.logger.debug('Back to Wi-Fi list')
        for loop in range(5):
            if self.device(resourceId="com.android.settings:id/switch_bar").exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        return False

    def open(self):
        '''validate wifi open status
         argv: To see available networks -- close
               wifi list -- open
        '''
        self.logger.debug('Open wifi')
        if self.device(text="OFF").exists:
            self.device(text="OFF").click()
        if self.device(textStartsWith='To see available networks').wait.gone(timeout=10000):
            self.device.delay(5)
            return True
        self.logger.debug('wifi open fail!!!')
        return False

    def close(self):
        '''validate wifi close status
         argv: To see available networks -- closed
               wifi list -- open
        '''
        self.logger.debug('Close wifi')
        if self.device(text="ON").exists:
            self.device(text="ON").click()
        if self.device(text="OFF").wait.exists(timeout=10000):
            return True
        self.logger.debug('wifi close fail!')
        return False

    def connect_wifi(self, hotspot, password, security="", ):
        self.enter()
        self.open()
        if self.wifi_status():
                self.logger.debug("Disconnect wifi at first")
                self.forget_wifi()
        self._connect(hotspot, password, security)

    def disconnect_wifi(self, hotspot):
        self.enter()
        self.forget(hotspot)
        self.close()
        self.back_to_home()

    def _connect(self, hotspot, password, security="", enter=False):
        '''device connect wifi hotspot
         argv: (str)hotspotName -- the wifi hotspot's name
               (str)password -- the wifi hotspot's password
               (str)security -- the password type
        '''
        self.logger.debug('Add hotspot --> ' + hotspot)
        if not self.enter():
            self.enter()
        self.open()
        if not self.device(text=hotspot).wait.exists(timeout = 1000):
            self.device(scrollable=True).scroll.vert.to(text=hotspot)
        if not self.device(text=hotspot).wait.exists(timeout = 1000):
            self.logger.info("can not find %s wifi" % hotspot)
            self.save_fail_img()
            return False
        self.device(text=hotspot).click()
        if password != "":
                self.device(resourceId="com.android.settings:id/password").set_text(password)
                self.device.delay(2)
        self.device(text="CONNECT").click.wait()
            

        # if More options have add network option, you can use this option to add wifi
        '''self.device(scrollable=True).scroll.vert.to(text="Add network")
        # self.device(description="More options").click()
        self.device(text="Add network").click.wait(timeout=2000)
        self.logger.debug("Input SSID/PWD/Security")
        if self.device(resourceId="com.android.settings:id/ssid").wait.exists(timeout=self.timeout):
            self.device(resourceId="com.android.settings:id/ssid").set_text(hotspot)
            if security != "":
                self.logger.debug("Select security")
                self.device(resourceId="com.android.settings:id/security").click()
                self.device(text=security).click.wait(timeout=2000)
                self.device.delay(1)
            if password != "":
                self.device(resourceId="com.android.settings:id/password").set_text(password)
                self.device.delay(2)
        self.logger.info(self.appconfig("wifi_connect", "Settings"))
        self.device(text=self.appconfig("wifi_connect", "Settings")).click.wait(timeout=2000)
        self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        if self.device(textStartsWith="Connected").wait.exists(timeout=50000):
            self.logger.debug('wifi connect success!!!')
            self.device.delay(1)
            return True
        else:
            self.logger.debug('can not find hotspot: %s', hotspot)
            return False'''

    def forget(self, hotpot):
        '''device forget wifi hotpot
         argv: (str)hotpotName -- the wifi hotpot's name
        '''
        self.logger.debug('forget hotpot')
        self.logger.debug('Search hotpot-------> ' + hotpot)
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(text=hotpot)
        if self.device(text=hotpot).wait.exists(timeout=30000):
            self.device(text=hotpot).click()
            if self.device(text="FORGET").wait.exists(timeout=2000):
                self.device(text="FORGET").click()
                if self.device(text="Connected").wait.gone(timeout=3000):
                    self.device.delay(1)
                    return True
                else:
                    self.logger.info("forget hotpot %s failed" % hotpot)
                    self.save_fail_img()
                    return False
            else:
                self.logger.info(hotpot + ' is not connected!!!')
                self.device.press.back()
                return True
            
    def forget_wifi(self):
        """disconnect wifi spot.

        author: Zhihao.Gu
        """
        self.logger.debug("Forget the Wifi")
        if self.device(textStartsWith="Connected").exists:
            self.device(textStartsWith="Connected").click()
            self.device.delay(3)
        if self.device(text="FORGET").wait.exists(timeout=3000):
            self.device(text="FORGET").click()
            self.device.delay(13)
            if self.device(text="FORGET").exists:
                self.logger.warning("Cannot forget the Wifi!")
                return False
            else:
                return True
        else:
            self.logger.warning("No popup Forget confirmation window!")
            return False

    def open_quick_wifi(self, ssid):
        self.device.open.quick_settings()
        self.device.delay()
        if self.device(text=ssid).wait.exists(timeout=2000):
            self.logger.info("wifi is connected to %s" % ssid)
            return True
        else:
            self.logger.info("wifi is off, open wifi from quick setting and connect %s" % ssid)
            self.device(description="Wi-Fi Off,Open Wi-Fi settings.", className="android.widget.Button").click()
            if self.device(textContains='Connected').wait.exists(timeout=30000):
                self.logger.debug("Wi-Fi is on, connect %s success" % ssid)
                return True
            else:
                self.logger.debug("open wifi fail!!!")
                self.save_fail_img()
                return False

    def close_quick_wifi(self, ssid):
        self.device.open.quick_settings()
        self.device.delay()
        if self.device(description="Wi-Fi Off,Open Wi-Fi settings.", className="android.widget.Button").wait.exists():
            self.logger.info("wifi is off")
            return True
        else:
            self.logger.info("wifi is on, close wifi from quick setting and disconnect %s" % ssid)
            if self.device(description='Wi-Fi three bars.').exists:
                self.device(description='Wi-Fi three bars.').click()
            elif self.device(description='Wi-Fi signal full.').exists:
                self.device(description='Wi-Fi signal full.').click()
            elif self.device(description="Wi-Fi disconnected.").exists:
                self.device(description="Wi-Fi disconnected.").click()
            else:
                self.device(text=ssid).click()
                self.device(text="ON").click()
            if self.device(description="Wi-Fi Off,Open Wi-Fi settings.", className="android.widget.Button").wait.exists(timeout=30000):
                self.logger.debug("close wifi success")
                return True
            else:
                self.logger.debug("close wifi fail!!!")
                self.save_fail_img()
                return False

    def web_refresh(self):
        '''switch wifi in quick settings panel and refresh website
        '''
        self.device.press.home()
        self.start_app("Chrome")
        self.chrome.browser_webpage(self.appconfig("wifiaddress", "Settings"))
        self.device(description = "More options").click()
        if self.device(description = "Refresh page").wait.exists(timeout = 20000) :
            self.device(description = "Refresh page").click()
            if self.device(resourceId=self.appconfig.id("id_progress", "Chrome")).wait.gone(timeout=30000):
                self.logger.debug("Website refresh success")
            else:
                self.logger.debug("Website refresh " + str(loop + 1) + " times failed.")
                self.save_fail_img()
                self.chrome.exit()
                return False
        self.chrome.exit()
        return True

    def wifi_status(self):
        """Check the wifi connected

        author: Zhx
        """
        self.logger.debug("Check the wifi status")
        if self.device(text='Internet not available').wait.exists(timeout=15000):
            if self.device(text='Cancel').exists:
                self.device(text='Cancel').click()
        self.device.delay(10)
        if self.device(textStartsWith="Connected").exists:
            self.logger.debug("WiFi connected")
            return True
        else:
            self.logger.debug("WiFi disconnected")
            return False


    def open_close_wifi(self):
        '''open / close wifi
         argv: To see available networks -- closed
               wifi list -- open
        '''
        self.logger.debug('Switch wifi')
        if self.close() and self.open():
            if self.device(textStartsWith="Connected").wait.exists(timeout=40000):
                self.logger.debug('wifi connect success!!!')
                self.device.delay(1)
                return True
            else:
                self.logger.debug('wifi connect fail!!!')
                self.save_fail_img()
                return False

    def enter_hotspot(self):
        self.logger.info("enter hotspot")
        self.enter_settings("More")
        if self.device(text = "Mobile Hotspot and Tethering").wait.exists(timeout = 2000) :
            self.device(text = "Mobile Hotspot and Tethering").click()
        else :
            self.logger.warning("Cannot enter more")

    def create_wifi_hotspot(self, ssid, password):
        self.logger.info("create %s wifi hotspot and open hotspot" % ssid)
        self.device(text = "Mobile HotSpot settings").click()
        self.device.delay(1)
        self.device(text="Set up Wi‑Fi hotspot").click()
        self.device(resourceId="com.android.settings:id/ssid").clear_text()
        self.device(resourceId="com.android.settings:id/ssid").set_text(ssid)
        self.device(resourceId="com.android.settings:id/password").set_text(password)
        self.device(text="SAVE").click()
        if self.device(text="%s WPA2 PSK portable Wi‑Fi hotspot" % ssid).wait.exists(timeout=20000):
            self.device.press.back()
            if self.open_hotspot() :
                self.logger.info("create %s wifi hotspot and open hotspot success" % ssid)
                return True
        self.logger.info("create %s wifi hotspot and open hotspot failed" % ssid)
        self.save_fail_img()
        return False
        
    def open_hotspot(self) :
        self.logger.info("open wifi hotspot")
        self.device(text="Wi-Fi Hotspot").click.wait(timeout=2000)
        if self.device(text = "Warning").wait.exists(timeout =2000) :
            self.device(text = "Don't show this message again").click.wait(timeout = 1000)
            self.device(text = "OK").click.wait(timeout = 1000)
        self.device.delay(2)
        self.device.open.notification()
        if self.device(text = "Tethering or hotspot active").wait.exists(timeout = 5000) :
            self.logger.debug("open wifi hotspot success")
            self.device.delay(2)
            self.device.press.back()
            return True
        self.logger.debug("open wifi hotspot failed")
        return False
        
        

    def close_hotspot(self):
        self.logger.info("close wifi hotspot")
        self.device.delay(2)
        self.device.open.notification()
        self.device.delay(1)
        if not self.device(text = "Tethering or hotspot active").wait.exists(timeout = 2000) :
            self.logger.debug("wifi hotspot already close")
            return True
        self.device.press.back()
        self.device(text="Wi-Fi Hotspot").click.wait(timeout=2000)
        self.device.delay(1)
        self.device.open.notification()
        if not self.device(text = "Tethering or hotspot active").wait.exists(timeout = 2000) :
            self.logger.debug("wifi hotspot already close")
            self.device.delay(1)
            self.device.press.back()
            return True
        self.logger.debug("close wifi hotspot failed")
        return False
        
    def open_close_hotspot(self):
        '''open / close hotspot
         argv: To see available networks -- closed
               wifi list -- open
        '''
        self.logger.debug('Switch hotspot')
        if self.open_hotspot() and self.close_hotspot():
            self.logger.debug('wifi hotspot switch success!!!')
            self.device.delay(1)
            return True
        else:
            self.logger.debug('wifi hotspot switch fail!!!')
            self.save_fail_img()
            return False
        
        
    def connect_hotspot(self):
        self.logger.info("s-device connect wifi hotspot and browser web page")
        self.sdevice.open.quick_settings()
        self.sdevice(description="Wi-Fi").click.wait(timeout=2000)
        if self.sdevice(text="Always").wait.exists(timeout=2000):
            self.sdevice(text="Wi-Fi").click()
            self.sdevice(text="Always").clcik()
        self.device()


class Airplane(Settings):
    def enter(self):
        self.enter_settings("More")

    def switch(self, status="OFF"):
        self.logger.debug('Switch airplane %s' % status)
        self.device.delay(1)
        check = "false" if status == "OFF" else "true"
        if self.device(resourceId="com.android.settings:id/list").child(index=0).child(checked=check,
                                                                          className='android.widget.Switch'):
            self.logger.info("airplane status is %s" % status)
            return True
        else:
            self.device(resourceId="com.android.settings:id/list").child(index=0).child(className='android.widget.Switch').click()
            self.device.delay(3)
            if self.device(resourceId="com.android.settings:id/list").child(index=0).child(checked=check,
                                                                              className='android.widget.Switch'):
                self.logger.info("Switch airplane %s success" % status)
                self.device.delay(2)
                return True
            self.logger.info("Switch airplane %s failed" % status)
            self.save_fail_img()
            return False


class Bt(Settings):
    def enter(self):
        return self.enter_settings("Bluetooth")

    def switch(self, status="OFF"):
        self.logger.debug('Switch BT %s' % status)
        if self.device(text=status).exists:
            self.logger.info("location status is %s" % status)
            return True
        else:
            self.device(resourceId="com.android.settings:id/switch_widget").click()
            if self.device(text=status).wait.exists(timeout=3000):
                self.logger.info("Switch BT %s success" % status)
                self.device.delay(2)
                return True
            self.logger.info("Switch BT %s failed" % status)
            self.save_fail_img()
            return False

    def enter_s(self):
        return self.enter_settings_s("Bluetooth")
        
    def switch_s(self, status):
        self.logger.debug("s-device switch %s" % status)
        if self.sdevice(text=status).exists:
            self.logger.info("s-device location status is %s" % status)
            return True
        else:
            self.sdevice(resourceId="com.android.settings:id/switch_widget").click()
            if self.sdevice(text=status).wait.exists(timeout=3000):
                self.logger.info("s-device Switch BT %s success" % status)
                self.device.delay(2)
                return True
            self.logger.info("s-device Switch BT %s failed" % status)
            self.save_fail_img_s()
            return False

    def compare(self):
        self.logger.info("m-device compare s-device")
        if self.device(text="ALCATEL ONETOUCH POP5").wait.exists(timeout=10000):
            self.logger.info("s-device bluetooth exists")
            self.device(text="ALCATEL ONETOUCH POP5").click()
            self.sdevice(text="PAIR").wait.exists(timeout=5000)
            self.sdevice(text="PAIR").click()
            self.device(text="PAIR").click()
            if self.device(resourceId="com.android.settings:id/deviceDetails").wait.exists(timeout=10000):
                self.logger.info("m-device compare s-device success")
                return True
            else:
                self.logger.info("m-device compare s-device failed")
                self.save_fail_img()
                return False
        else:
            self.logger.info("s-device bluetooth not exists")
            self.save_fail_img()
            return True

    def cancel_compare(self):
        self.logger.info("m-device cancel compare s-device")
        self.device(resourceId="com.android.settings:id/deviceDetails").click()
        self.device.delay()
        self.device(text="FORGET").click()
        self.device.delay()
        if not self.device(resourceId="com.android.settings:id/deviceDetails").exists:
            self.logger.info("m-device cancel compare s-device success")
            return True
        else:
            self.logger.info("m-device cancel compare s-device failed")
            self.save_fail_img()
            return False

    def transfer(self, filename="Copy.rar"):
        self.logger.info("m-device transfer %s file to s-device" % filename)
        self.back_to_home()
        self.start_app("Files")
        self.device(text="Phone").click()
        self.device(scrollable=True).scroll.vert.to(text=filename)
        x , y = self.device(text=filename).get_location()
        self.device.swipe(x, y, x + 1, y + 1, steps=300)
        self.device(resourceId='com.jrdcom.filemanager:id/share_btn').click.wait(timeout=2000)
        self.device(text='Bluetooth').click.wait(timeout=2000)
        self.device(text='ALCATEL ONETOUCH POP5').click.wait(timeout=2000)
        self.sdevice.open.notification()
        self.sdevice(text="ACCEPT").click()
        self.sdevice.open.notification()
        self.device.open.notification()
        for i in range(5):
            self.device.delay(60)
            self.logger.debug("transfering")
            if self.device(text="1 successful, 0 unsuccessful.").exists and self.sdevice(
                    text="1 successful, 0 unsuccessful.").exists:
                self.logger.info("m-device transfer %s file to s-device success" % filename)
                self.sdevice(description="Clear all notifications.").click()
                self.device(description="Clear all notifications.").click()
                self.back_to_home()
                return True
        self.logger.info("m-device transfer %s file to s-device failed" % filename)
        self.save_fail_img()
        self.back_to_home()
        return False


class GPS(Settings):

    def __init__(self, device, log_name, sdevice=None):
        Settings.__init__(self, device, log_name, sdevice)
        #self.settings = Settings(self.device, "GPS_ss")
        
    def enter(self):
        return self.enter_settings("Location")

    def switch(self, status="OFF"):
        self.logger.debug('Switch gps %s' % status)
        if self.device(text=status).exists:
            self.logger.info("location status is %s" % status)
            return True
        else:
            self.device(resourceId="com.android.settings:id/switch_widget").click()
            if self.device(text=status).wait.exists(timeout=3000):
                self.logger.info("Switch gps %s success" % status)
                self.device.delay(2)
                return True
            self.logger.info("Switch gps %s failed" % status)
            self.save_fail_img()
            return False


class NFC(Settings):
    def enter(self):
        return self.enter_settings("More")

    def switch(self, status="OFF"):
        self.logger.debug('Switch NFC %s' % status)
        self.device.delay(1)
        check = "false" if status == "OFF" else "true"
        if self.device(resourceId="com.android.settings:id/list").child(index=1).child(index=1).child(checked=check,
                                                                                         className='android.widget.Switch'):
            self.logger.info("NFC status is %s" % status)
            return True
        else:
            self.device(resourceId="com.android.settings:id/list").child(index=1).child(index=1).child(
                className='android.widget.Switch').click()
            self.device.delay(3)
            if self.device(resourceId="com.android.settings:id/list").child(index=1).child(index=1).child(checked=check,
                                                                                             className='android.widget.Switch'):
                self.logger.info("Switch NFC %s success" % status)
                self.device.delay(2)
                return True
            self.logger.info("Switch NFC %s failed" % status)
            self.save_fail_img()
            return False


class DualSim(Settings):
    def enter_sim(self):
        return self.enter_settings("SIM cards")

    def switch_sim(self, sim_card=1, switch="ON"):
        """sim_card 1,2
           switch  OFF ON
        """
        self.logger.info("switch sim card %d to %s" % (sim_card, switch))
        if switch == "OFF":
            if self.device(text="SIM %d is Disabled" % sim_card).wait.exists(timeout=2000):
                self.logger.info("sim card %d is OFF" % sim_card)
                return True
            self.device(index=sim_card, className="android.widget.LinearLayout").child(index=2).click()
            self.device(text="OK").click()
            self.device(text="OK").click.wait(timeout=5000)
            if self.device(text="SIM %d is Disabled" % sim_card).wait.exists(timeout=2000):
                self.logger.info("sim card %d switch to OFF success" % sim_card)
                return True
            self.logger.info("sim card %d switch to OFF failed" % sim_card)
            self.save_fail_img()
            return False
        else:
            if not self.device(text="SIM %d is Disabled" % sim_card).wait.exists(timeout=2000):
                self.logger.info("sim card %d is ON" % sim_card)
                return True
            self.device(index=sim_card, className="android.widget.LinearLayout").child(index=2).click()
            self.device(text="OK").click.wait(timeout=5000)
            if not self.device(text="SIM %d is Disabled" % sim_card).wait.exists(timeout=2000):
                self.logger.info("sim card %d switch ON success" % sim_card)
                return True
            self.logger.info("sim card %d switch ON failed" % sim_card)
            self.save_fail_img()
            return False

    def switch_data(self, sim_card=1, switch="ON"):
        self.logger.info("switch sim card data %d to %s" % (sim_card, switch))
        if self.device(resouceId="android:id/list").child(index=1).child(index=0).child(text=switch).wait.exists(
                timeout=2000):
            self.logger.info("sim card data %d is %s" % (sim_card, switch))
            return True
        self.device(resouceId="android:id/list").child(index=1).child(index=0).child(index=1).click()
        if self.device(resouceId="android:id/list").child(index=1).child(index=0).child(text=switch).wait.exists(
                timeout=2000):
            self.logger.info("switch sim card data %d to %s success" % (sim_card, switch))
            return True
        self.logger.info("switch sim card data %d to %s failed" % (sim_card, switch))
        self.save_fail_img()
        return False

    def enter_data(self, sim_card=1):
        self.enter_settings("Data usage")
        self.device(resouceId="android:id/tabs").child(index=sim_card - 1).click()
        
class WFC(Settings) :

    def __init__(self, device, log_name, sdevice=None):
        Settings.__init__(self, device, log_name, sdevice)
        
    def enter_s(self):
        return self.enter_settings_s("More")
        
    def open_wificalling(self):
        if self.device(textContains="Wi-Fi calling").exists:
            self.device(textContains="Wi-Fi calling").click()
            self.device.delay(2)
        #Jake
            if self.device(text = "On").wait.exists(timeout = 2000):
                self.logger.debug('wificalling open!')
                return True
            else:
                self.logger.debug('wificalling closed!')
                self.device(resourceId='com.android.settings:id/switch_widget').click()
                self.device.delay(1)
                if self.device(text = "On").wait.exists(timeout = 2000):
                    self.logger.debug('wificalling open!')
                    return True
        #End
        self.logger.debug('wificalling open fail!')
        return False
        
    def open_wificalling_s(self):
        if self.sdevice(textContains="Wi-Fi calling").exists:
            self.sdevice(textContains="Wi-Fi calling").click()
            self.sdevice.delay(2)
        #Jake
            if self.sdevice(text = "On").wait.exists(timeout = 2000):
                self.logger.debug('wificalling open!')
                return True
            else:
                self.logger.debug('wificalling closed!')
                self.sdevice(resourceId='com.android.settings:id/switch_widget').click()
                self.sdevice.delay(1)
                if self.sdevice(text = "On").wait.exists(timeout = 2000):
                    self.logger.debug('wificalling open!')
                    return True
        #End
        self.logger.debug('wificalling open fail!')
        return False
        
    def wificalling_opt(self,strtype):
        """switch wificalling_opt
        wifi preferred = wifipre
        wifi only = wifionly
        cellular preferred = cellularpre
        """
        wi_order = {'Wi-Fi preferred':0,'Wi-Fi Only':1,'Cellular preferred':2}
        if self.device(textContains="Calling preference").exists:
            self.device(textContains="Calling preference").click()
            self.device.delay(2)
        if self.device(text = strtype).wait.exists(timeout = 2000) :
            self.device(text = strtype).click()
            return True
        else :
            self.logger.warning("Cannot find this option")
            return False
            
    def wificalling_opt_s(self,strtype):
        """switch wificalling_opt
        wifi preferred = wifipre
        wifi only = wifionly
        cellular preferred = cellularpre
        """
        wi_order = {'Wi-Fi preferred':0,'Wi-Fi Only':1,'Cellular preferred':2}
        if self.sdevice(textContains="Calling preference").exists:
            self.sdevice(textContains="Calling preference").click()
            self.sdevice.delay(2)
        if self.sdevice(text = strtype).wait.exists(timeout = 2000) :
            self.sdevice(text = strtype).click()
            return True
        else :
            self.logger.warning("Cannot find this option")
            return False
            
    def back_end_call(self):
        """back to call page and end call
        """
        self.logger.info("back to the call and end the call")
        self.device.open.notification()
        if self.device(text="Ongoing call").wait.exists():
            self.device(text="Ongoing call").click()
            if self.device(description='End').wait.exists(timeout=2000):
                self.logger.info("back to call success")
                self.device(description="End").click()
                self.device.delay(1)
                if not self.device(description='End').exists:
                    self.logger.info("end call success")
                    return True
                else:
                    self.logger.info("end call failed")
                    self.save_fail_img()
                    return False
        else:
            self.logger.info("Call has ended")
            self.device.press.home()
            return True
    


'''if __name__ == '__main__':
    a = Wifi("80c08ac6", "Wifi")
    a.enter()
    a._connect("SOL(AM-H200)","11111111","WPA/WPA2 PSK")
    a.open_close_wifi()
    a.open_close_wifi()
    a.forget("SOL(AM-H200)")
    a.close()'''