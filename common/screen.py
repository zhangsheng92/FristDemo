# -*- coding: UTF-8 -*-
#__author__ = '93760'
from settings import Settings
from common import *
from automator.adb import Adb


class LockScreen(Common):
    def __init__(self, device, mod, sdevice=None):
        Common.__init__(self, device, mod, sdevice)
        self.set = Settings(self.device, "lock_set")

    def enter(self):
        self.set.enter_settings("Security")
        if self.device(text = "Screen lock").wait.exists(timeout = 2000) :
            self.device(text = "Screen lock").click()
            self.logger.debug("Enter Screen lock success")
            return True
        else :
            self.logger.debug("Cannot find Screen lock ")
            return False
        
    def swipe_screen(self):
        self.device.sleep()
        self.logger.info("device sleep")
        self.device.delay(1)
        self.device.wakeup()
        self.logger.info("device awake")
        self.device.delay(1)
        self.logger.info("swipe screen")
        self.device.swipe(341, 1105, 340, 100, 40)

    def lock_screen(self, lock_type, password=None):
        self.logger.info("%s lock screen" % lock_type)
        self.device.press.home()
        self.swipe_screen()
        self.device.delay(1)
        if lock_type != "Swipe":
            self.logger.info("enter %s password %s" % (lock_type, password))
            if lock_type == "PIN":
                for i in range(4) :
                    self.device(resourceId = "com.android.systemui:id/key1").click()
                    self.device.delay(0.5)
                self.device(resourceId="com.android.systemui:id/key_enter").click()
            elif lock_type == "Password":
                self.device(resourceId="com.android.systemui:id/passwordEntry").set_text(password)
                self.device.delay(1)
                self.device.press.enter()
            else :
                self.device.server.adb.shell("monkey -f /sdcard/monkey1.txt 1")
                self.device.delay(1)
        if self.device(description="Apps").wait.exists(timeout=2000):
            self.logger.info("%s lock screen success" % lock_type)
            return True
        self.logger.info("%s lock screen failed" % lock_type)
        self.save_fail_img()
        return False

    def switch_lock_to_none(self, lock_type, password=None):
        """Swipe PIN Password
        """
        self.logger.info("switch %s lock type to None" % lock_type)
        self.enter()
        self.device.delay(1)
        self.device.delay(1)
        if lock_type == "Swipe":
            self.device(text="None").click()
        elif lock_type == "Pattern" :
            self.device.server.adb.shell("monkey -f /sdcard/monkey.txt 1")
            self.device.delay(1)
            self.device(text="None").click()
            self.device(text="YES, REMOVE").click()
        else :
            self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
            self.device.press.enter()
            self.device(text="None").click()
            self.device(text="YES, REMOVE").click()
        if self.device(text="None").wait.exists(timeout=2000):
            self.logger.info("switch %s lock type to None success" % lock_type)
            self.back_to_home()
            return True
        self.logger.info("switch %s lock type to None failed" % lock_type)
        self.save_fail_img()
        self.back_to_home()
        return False

    def switch_lock_to_lock(self, lock_type, password=None):
        """Swipe PIN Password
        """
        self.logger.info("switch None lock to %s lock type" % lock_type)
        self.enter()
        self.device(text=lock_type).click()
        self.device.delay(1)
        if lock_type != "Swipe":
            self.device(text="No thanks").click()
            if lock_type == "Pattern" :
                self.device.server.adb.shell("monkey -f /sdcard/monkey.txt 1")
                self.device.delay(1)
                self.device(text = "CONTINUE").click()
                self.device.delay(1)
                self.device.server.adb.shell("monkey -f /sdcard/monkey.txt 1")
                self.device(text = "CONFIRM").click()
            else :
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                self.device.press.enter()
                self.device(resourceId="com.android.settings:id/password_entry").set_text(password)
                self.device.press.enter()
            self.device.delay(1)
            self.device(text="DONE").click()
        if self.device(text=lock_type).wait.exists(timeout=2000):
            self.logger.info("switch None lock to %s lock type success" % lock_type)
            self.back_to_home()
            return True
        self.logger.info("switch None lock to %s lock type failed" % lock_type)
        self.save_fail_img()
        self.back_to_home()
        return False

    def switch_wallpaper(self, index=0):
        self.logger.info("switch wallpaper to %d" % (index % 2))
        self.device.press.home()
        self.device(resourceId='com.tct.launcher:id/launcher').long_click()
        self.device.delay(1)
        self.device(resourceId='com.tct.launcher:id/wallpaper_button').click()
        self.device.delay(2)
        self.device(resourceId='com.tct.launcher:id/wallpaper_list').child(index=index % 2).click()
        self.device(text='Set wallpaper').click()
        self.device(text='Home screen').click()
        if self.device(description="Apps").wait.exists(timeout=2000):
            self.logger.info("switch wallpaper to %d success" % (index % 2))
            return True
        self.logger.info("switch wallpaper to %d failed" % (index % 2))
        self.save_fail_img()
        return False


if __name__ == "__main__":
    a = LockScreen("2cb8d833", "LockScreen")
    # a.enter()
    a.swipe_screen()