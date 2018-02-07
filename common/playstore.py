import re
import sys
from common import *
from _socket import timeout


class PlayStore(Common):
    """Provide common functions involved Play Store."""

    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self.appconfig.set_section("Store")

    def enter(self):
        """enter play store.
        """
        self.logger.debug('enter play store')
        if self.device(resourceId="com.android.vending:id/search_box_idle_text").wait.exists(timeout=self.timeout):
            return True
        self.start_app(self.appconfig("name"))
        self.device.delay(2)
        self.back_main_app()
        if self.device(resourceId="com.android.vending:id/search_box_idle_text").wait.exists(timeout=self.timeout):
            return True
        else:
            self.logger.warning('enter play store fail!')
            self.save_fail_img()
            return False

    def exit(self):
        """exit play store.
        """
        self.logger.debug('exit play store')
        for loop in range(4):
            if self.device(packageName="com.tct.launcher").wait.exists(timeout=2000):
                self.device.press.home()
                return True
            self.device.press.back()
        self.logger.debug('exit play store fail!!!')
        self.save_fail_img()
        return False

    def back_main_app(self):
        '''back to play store main screen
        '''
        for loop in range(5):
            if self.device(description="Show navigation drawer").wait.exists(timeout=1000):
                return True
            self.device.press.back()
        self.logger.warning("Cannot back to main app")
        return False

    def check_interface(self):
        '''check interface in APPS&GAMES / Account&Settings
        '''
        return self.check_apps() and self.check_account() and self.check_setting()
        
        
    def check_category(self):
        """Check play store category.

        author: Zhx
        """
        self.logger.debug("Check play store category")
        if not self.device(resourceId="com.android.vending:id/search_box_idle_text").exists :
            self.logger.warning("Cannnot enter the play store home page!")
            return False
        self.logger.debug("Enter the play store success")
        return True

    def check_apps(self):
        self.logger.debug("Check Apps,Games,Movies,Books top free,top paid interface.")
        for application in ["APPS", "GAMES", "MOVIES", "BOOKS"]:
            self.logger.info("Check %s top free& top paid interface."%application)
            if application in ["APPS", "GAMES"]:
                self.device(text="APPS & GAMES").click()
                if application!="APPS":
                    self.device(text=application).click()
                if self.device(text="TOP CHARTS").wait.exists(timeout=5000):
                    self.logger.info("login %s success"%application)
                else:
                    self.logger.info("login %s failed"%application)
                    self.save_fail_img()
                    return False
                self.device(text="TOP CHARTS").click()
                for mark in ["TOP PAID", "TOP GROSSING"]:
                    self.device(text=mark).click()
                    if self.device(resourceId="com.android.vending:id/play_card").wait.exists(timeout=5000):
                        self.logger.info("Check Apps %s success"%mark)
                    else:
                        self.logger.info("Check Apps %s failed"%mark)
                        self.save_fail_img()
                        return False
            else:
                self.device(text="ENTERTAINMENT").click()
                self.device(text=application).click()
                for mark in ["TOP SELLING", "NEW RELEASES"]:
                    self.device(text=mark).click()
                    if self.device(resourceId="com.android.vending:id/play_card").wait.exists(timeout=10000):
                        self.logger.info("Check Apps %s success"%mark)
                    else:
                        self.logger.info("Check Apps %s failed"%mark)
                        self.save_fail_img()
                        return False
                    self.device.press.back()
                self.device.press.back()
            self.back_main_app()
        self.logger.debug("Check Apps,Games,Movies,Books top free,top paid interface success.")
        return True

    def check_account(self):
        self.logger.info("Check interface my account")
        self.back_main_app()
        self.device(description="Show navigation drawer").click.wait()
        if self.device(text="My account").exists:
            self.device(text="My account").click()
            if self.device(text="Add payment method").wait.exists(timeout=5000):
                self.logger.info("Check interface my account success")
                self.device.press.back()
                return True
        else:
            self.device(text="Account").click()
            if self.device(text="Payment methods").wait.exists():
                self.logger.info("Check interface my account success")
                self.device.press.back()
                return True
        self.logger.info("Check interface my account success")
        self.save_fail_img()
        self.back_main_app()
        return False

    def check_setting(self):
        self.logger.info("Check interface setting")
        self.back_main_app()
        self.device(description="Show navigation drawer").click.wait()
        self.device(scrollable=True).scroll.vert.toEnd()
        self.device(text="Settings").click()
        if self.device(text="Auto-update apps").wait.exists(timeout=5000):
            self.logger.info("Check interface setting success")
            self.device.press.back()
            return True
        else:
            self.logger.info("Check interface setting success")
            self.save_fail_img()
            self.back_main_app()
            return False

    def download_open_apk(self, apk="TCTTemperature"):
        self.logger.info("download and open apk %s"%apk)
        self.logger.info("search %s apk" % apk)
        self.device(resourceId="com.android.vending:id/search_box_idle_text").click()
        self.device(resourceId="com.android.vending:id/search_box_text_input").set_text("TCTTemperature")
        self.device.press.enter()
        if self.device(text=apk, resourceId="com.android.vending:id/li_title").wait.exists(timeout=20000):
            self.device(text=apk, resourceId="com.android.vending:id/li_title").click()
            self.device.delay(5)
            if self.device(text="UNINSTALL").exists:
                self.device(text="UNINSTALL").click()
                self.device(text="OK").click()
                self.device.delay(5)
            self.logger.debug("download and Install %s apk." % apk)
            self.device(text="INSTALL").click.wait()
            self.device(text="ACCEPT").click()
            if self.device(text="OPEN").wait.exists(timeout=30000):
                self.logger.debug("download and Install %s apk success." % apk)
                self.logger.info("open %s apk" % apk)
                self.device(text="OPEN").click()
                if self.device(text="Temperature of your battery").wait.exists(timeout=5000):
                    self.logger.info("open %s apk success" % apk)
                    self.device.press.back()
                    self.logger.info("uninstall %s apk" % apk)
                    self.device(text="UNINSTALL").click()
                    self.device(text="OK").click()
                    if self.device(text="INSTALL").wait.exists(timeout=10000):
                        self.logger.info("uninstall %s apk success" % apk)
                        return True
                    else:
                        self.logger.info("uninstall %s apk failed" % apk)
                        self.save_fail_img()
                        return False
                else:
                    self.logger.info("open %s apk failed" % apk)
                    self.save_fail_img()
                    return False
            else:
                self.logger.debug("Install %s apk failed." % apk)
                self.save_fail_img()
                return False
        else:
            self.logger.info("Search %s apk failed." % apk)
            self.save_fail_img()
            return False


if __name__ == '__main__':
    a = PlayStore("80c08ac6", "PlayStore")
    a.enter()
    a.download_open_apk()
    a.back_main_app()