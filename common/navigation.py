# -*- coding: UTF-8 -*-
"""Telephony library for scripts.
"""
from common import *


class MenuNavigation(Common):

    def _apps_navigation(self):
        self.logger.info("start 16 apps from navigation interface")
        self.device.press.home()
        self.device(description="Apps").click()
        self.device().scroll.vert.toBeginning()
        self.device.press.home()
        for i in range(16):
            self.device(description="Apps").click()
            self.device(resourceId="com.tct.launcher:id/icon",index=i+1).click.wait(timeout=2000)
            self.device.delay(2)
            if not self.device(description="Search Apps…").exists:
                self.logger.info("start %dth app success" % (i + 1))
            else:
                self.logger.info("start %dth app failed" % (i + 1))
                return False
            self.device.press.home()
        self.logger.info("start 16 apps from navigation interface success")
        return True

    def _launcher_navigation(self):
        self.logger.info("start apps from launcher interface")
        self.device.press.home()
        for i in range(5):
            self.device(resourceId="com.tct.launcher:id/layout").child(className='android.view.ViewGroup', index=1).child(index=i).click()
            self.device.delay(2)
            if not self.device(packageName="com.tct.weather").exists:
                self.logger.info("start %dth app success" % (i + 1))
            else:
                self.logger.info("start %dth app failed" % (i + 1))
                return False
            self.device.press.home()
            self.device.delay(2)
        self.logger.info("start apps from launcher interface success")
        self.device.press.home()
        return True

if __name__ == '__main__':
    a = MenuNavigation("80c08ac6", "MenuNavigation")
    # a.device(resourceId="com.tct.launcher:id/icon", index=6).click()
    a._apps_navigation()
    # print a.device.dump()

