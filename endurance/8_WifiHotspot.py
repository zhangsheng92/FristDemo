#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.settings import Wifi
from common.chrome import Chrome


class WifiHotspotEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mdevice = "MDEVICE"
        sdevice = "SDEVICE"
        if len(sys.argv) > 1:
            mdevice = sys.argv[1]
            sdevice = sys.argv[1]
        cls.mod = Wifi(mdevice, "WifiHotspot")
        cls.wifi = Wifi(sdevice, "open_wifi")
        cls.chrome = Chrome(cls.wifi.device, "browser_web")
        cls.ssid = cls.mod.config.getstr("wifi_name", "Wifi", "common")
        cls.pwd = cls.mod.config.getstr("wifi_password", "Wifi", "common")
        cls.security = cls.mod.config.getstr("wifi_security", "Wifi", "common")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('WifiHotspot Mission Complete')
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        rate = cls.mod.suc_times / cls.mod.test_times * 100
        if rate < 95:
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(rate) + '%')

    def setUp(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def tearDown(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def test_hotspot(self):
        self.case_wifi_hotspot(int(self.mod.dicttesttimes.get("hotspot_connect_times".lower())))
        self.case_switch_hotspot(int(self.mod.dicttesttimes.get("hotspot_switch".lower())))
        self.case_wifi_switch(self.ssid, self.pwd, self.security,int(self.mod.dicttesttimes.get("wifi_switch".lower())))

    def case_wifi_hotspot(self, times):
        self.mod.logger.info("wifi hotspot open、close、connect %d times" % times)
        self.mod.enter_hotspot()
        for loop in range(times):
            try:
                ssid = self.mod.random_name(loop)
                password = self.mod.random_name(loop)
                if self.mod.create_wifi_hotspot(ssid, password) :
                    self.wifi._connect(ssid, password, 'WPA/WPA2 PSK', enter=True)
                    if self.chrome.browser_webpage():
                        self.mod.suc_times += 1
                        self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.error(e)
                self.mod.save_fail_img()
                self.wifi.save_fail_img()
            finally:
                self.chrome.exit()
                self.wifi.enter()
                self.wifi.close()
                self.wifi.back_to_home()
                self.mod.close_hotspot()
        self.mod.back_to_home()
        self.mod.logger.info("wifi hotspot open、close、connect %d times" % times)
        
    def case_wifi_switch(self, ssid, pwd, security, times=1):
        '''case:connect wifi in wifi settings
        '''
        self.mod.logger.debug("Dis/Connect Wifi %s Times." % times)
        self.mod.connect_wifi(ssid, pwd, security)
        for loop in range(times):
            try:
                if self.mod.open_close_wifi() and self.mod.close_quick_wifi(ssid) and self.mod.open_quick_wifi(ssid):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop " + str(loop + 1))
            except Exception, e:
                self.mod.logger.error(e)
                self.mod.save_fail_img()
            finally:
                self.mod.back_to_wifi()
        self.mod.back_to_home()
        self.mod.logger.debug("Wifi Connect And Disconnect Test Mission Complete")
        
    def case_switch_hotspot(self , times=1):
        '''case:connect wifi in wifi settings
        '''
        self.mod.logger.debug("open/off WifiHotspot %s Times." % times)
        self.mod.enter_hotspot()
        for loop in range(times):
            try:
                if self.mod.open_close_hotspot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop " + str(loop + 1))
            except Exception, e:
                self.mod.logger.error(e)
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.debug("Wifi Connect And Disconnect Test Mission Complete")


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(WifiHotspotEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite)