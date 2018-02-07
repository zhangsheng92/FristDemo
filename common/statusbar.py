# -*- coding: UTF-8 -*-
from common import *


class StatusBar(Common):

    def switch_gps(self, status):
        """OFF ON
        """
        self.logger.info("switch gps to %s" % status)
        self.device.delay(1)
        if not self.device(text = "Location").wait.exists(timeout = 2000) :
            self.logger.debug("swipe left")
            self.device(className = "android.support.v4.view.ViewPager").swipe.left()
        if self.device(description="Location reporting %s." % status.lower()).wait.exists(timeout=2000):
            self.logger.info("gps status is %s" % status)
            return True
        else:
            self.device(text="Location").click()
            if self.device(description="Location reporting %s." % status.lower()).wait.exists(timeout=2000):
                self.logger.info("switch gps to %s success" % status)
                self.device.delay()
                return True
            else:
                self.logger.info("switch gps to %s failed" % status)
                self.save_fail_img()
                return False

    def switch_nfc(self, status):
        """OFF ON
        """
        self.logger.info("switch NFC to %s" % status)
        self.device.delay(1)
        if self.device(description="NFC turned %s." % status.lower()).exists:
            self.logger.info("NFC status is %s" % status)
            return True
        else:
            self.device(text="NFC").click()
            if self.device(description="NFC turned %s." % status.lower()).wait.exists(timeout=2000):
                self.logger.info("switch NFC to %s success" % status)
                self.device.delay()
                return True
            else:
                self.logger.info("switch NFC to %s failed" % status)
                self.save_fail_img()
                return False

    def switch_bt_off(self):
        self.logger.info("switch bt to OFF")
        self.device.delay(1)
        #Bluetooth off.,Open Bluetooth settings.
        if self.device(description="Bluetooth off.,Open Bluetooth settings.").exists:
            self.logger.info("Bluetooth status is off.")
            return True
        else:
            self.logger.info("Bluetooth is on, close bt from quick setting.")
            self.device(text="Bluetooth").click()
            self.device.delay(1)
            self.device(text="ON").click()
            if self.device(description="Bluetooth off.,Open Bluetooth settings.").wait.exists(timeout=2000):
                self.logger.info("switch bt off success")
                self.device.delay()
                return True
            else:
                self.logger.info("switch bt to off failed")
                self.save_fail_img()
                return False

    def switch_bt_on(self):
        self.logger.info("switch bt to ON")
        self.device.delay(1)
        #Bluetooth off.,Open Bluetooth settings.
        if self.device(description="Bluetooth on.,Not connected.,Open Bluetooth settings.").exists:
            self.logger.info("Bluetooth status is ON.")
            return True
        else:
            self.logger.info("Bluetooth is off, open bt from quick setting.")
            self.device(text="Bluetooth").click()
            self.device.delay(1)
            self.device(text="ON").wait.exists(timeout=2000)
            self.device(resourceId="android:id/up").click()
            if self.device(description="Bluetooth on.,Not connected.,Open Bluetooth settings.").wait.exists(timeout=2000):
                self.logger.info("switch bt ON success")
                self.device.delay()
                return True
            else:
                self.logger.info("switch bt to ON failed")
                self.save_fail_img()
                return False

    def switch_wifi(self):
        self.logger.debug('Switch wifi')
        wifi_switcher = self.device(resourceId="com.android.systemui:id/quick_settings_panel").child(index=2).child(
            index=0)
        if self.device(description='Wi-Fi is off.'):
            wifi_switcher.click()
            if self.device(description='Wi-Fi is off.').wait.gone(timeout=10000):
                self.logger.debug('wifi is opened!')
                return True
            else:
                self.logger.debug('wifi open fail!!!')
                return False
        else:
            wifi_switcher.click()
            if self.device(description='Wi-Fi is off.').wait.exists(timeout=10000):
                self.logger.debug('wifi is closed!')
                return True
            else:
                self.logger.debug('wifi close fail!!!')
                return False

    def switch_airplane(self, status="OFF"):
        self.logger.info("switch airplane to %s" % status)
        check = "false" if status == "OFF" else "true"
        self.device.delay(1)
        if self.device(description="Airplane mode", checked=check).exists:
            self.logger.info("airplane status is %s" % status)
            return True
        else:
            self.device(description="Airplane mode").click()
            if self.device(description="Airplane mode", checked=check).wait.exists(timeout=2000):
                self.logger.info("switch airplane to %s success" % status)
                self.device.delay()
                return True
            else:
                self.logger.info("switch airplane to %s failed" % status)
                self.save_fail_img()
                return False