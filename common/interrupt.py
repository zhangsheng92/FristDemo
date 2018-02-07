# -*- coding: UTF-8 -*-
"""Maps interrupt library for scripts.
"""
from common import *
from telephony import Telephony


class GoogleMapsInterrupt(Common):

    def __init__(self, device, log_name, sdevice=None):
        Common.__init__(self, device, log_name, sdevice)
        self.tel = Telephony(self.device, "maps_tel", self.sdevice)
        self.tel.mdevice_tel = self.mdevice_tel
        self.tel.mdevice_msg = self.mdevice_msg
        self.tel.sdevice_tel = self.sdevice_tel

    def enter(self):
        """Launch google maps
        """
        self.logger.debug('enter google maps')
        self.start_app("Maps")
        return self.device(resourceId="com.google.android.apps.maps:id/search_omnibox_text_box").wait.exists()

    def back_to_maps(self):
        self.logger.info("Back to maps.")
        for i in range(4):
            if self.device(resourceId="com.google.android.apps.maps:id/search_omnibox_text_box").wait.exists(timeout=1000):
                self.device(description="Clear").click()
                return
            else:
                self.device.press.back()
        self.enter()
        for i in range(4):
            if self.device(text="Search here").wait.exists(timeout=1000):
                return
            else:
                self.device.press.back()

    def navigation(self):
        """determine whether the navigation, return True/False
        """
        if self.device(description="Audio level selector button").wait.exists(timeout=5000):
            self.logger.info("Navigation....")
            return True
        self.logger.info("Navigation fail!!!")
        self.save_fail_img()
        return False

    def maps_navigation(self):
        """start google maps, enter the navigation
        """
        destination = Configs("common").get("destination", "Maps")
        self.logger.debug("Search: %s" % destination)
        self.device(resourceId="com.google.android.apps.maps:id/search_omnibox_text_box").click()
        self.device(resourceId="com.google.android.apps.maps:id/search_omnibox_edit_text").set_text(destination)
        self.device.press.enter()
        if self.device(text="The University of Nottingham Ningbo （Southeast Gate）").wait.exists():
            self.device(text="The University of Nottingham Ningbo （Southeast Gate）").click()
        self.logger.debug("Start navigation to: %s" % destination)
        if self.device(description="Directions").wait.exists(timeout=10000):
            self.device(description="Directions").click()
            self.device.delay(5)
            self.device(description="Start navigation").click.wait(timeout=3000)
            if self.device(description="GOT IT").wait.exists(timeout=3000):
                self.device(description="GOT IT").click()
            return self.navigation()
        else:
            self.logger.info("search out time")
            self.save_fail_img()
            return False

    def answer_navigation(self):
        """answer call during maps navigation
        """
        if self.tel.s_call():
            self.logger.debug("answer call during maps interrupt success")
            return True
        self.logger.debug("answer call during maps interrupt failed")
        self.save_fail_img()
        return False

    def back_navigation(self):
        """after calling  whether the navigation, return True/False
        """
        self.device.delay(5)
        #self.device(description="End").click()
        self.device.click(720, 2210)
        if self.device(description="End").wait.gone():
            self.logger.info("answer call during maps interrupt success")
            return self.navigation()
        self.logger.info("answer call during maps interrupt failed")
        self.save_fail_img()
        return False

    def open_location(self):
        self.logger.info("open location")
        self.start_app("Settings")
        self.device(scrollable=True).scroll.vert.to(text="Location")
        self.device(text="Location").click()
        if self.device(text="OFF").wait.exists():
            self.device(text="OFF").click()
        if self.device(text="ON").wait.exists():
            self.logger.info("open location success")
        else:
            self.logger.info("open location failed")
        self.device.press.back()
        self.device.press.back()

    def close_location(self):
        self.logger.info("close location")
        self.start_app("Settings")
        self.device(scrollable=True).scroll.vert.to(text="Location")
        self.device(text="Location").click()
        if self.device(text="ON").wait.exists():
            self.device(text="ON").click()
        if self.device(text="OFF").wait.exists():
            self.logger.info("close location success")
        else:
            self.logger.info("close location failed")
        self.device.press.back()
        self.device.press.back()


if __name__ == '__main__':
    a = GoogleMapsInterrupt("80c08ac6", "Maps", "e3a1b0f2")
    # a.open_location()
    # a.enter()
    # a.maps_navigation()
    a.answer_navigation()
    a.back_navigation()
    # a.close_location()

