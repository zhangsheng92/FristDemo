# -*- coding: UTF-8 -*-
__author__ = '93760'
"""Camera library for scripts.
"""

from common import Common


class FM(Common):

    def enter(self):
        """Launch music by StartActivity.
        """
        self.logger.debug('enter fm')
        if self.device(resourceId="com.tct.fmradio:id/menu_audio_mode").wait.exists(timeout=5000):
            return True
        self.start_app("Radio", b_desk=False)
        while self.device(text = "YES").wait.exists(timeout = 2000) :
            self.device(text = "YES").click()
            self.device.delay(1)
        while self.device(text = "ALLOW").wait.exists(timeout = 2000) :
            self.device(text = "ALLOW").click()
            self.device.delay(1)
        while self.device(text = "CONTINUE").wait.exists(timeout = 2000) :
            self.device(text = "CONTINUE").click()
            self.device.delay(1)
        if self.device(resourceId="com.tct.fmradio:id/menu_audio_mode").wait.exists(timeout=5000):
            return True
        else:
            self.logger.warning('enter fm fail!')
            return False

    def exit(self):
        self.logger.info("exit radio")
        self.device.delay(2)
        if self.device(description="More options").exists:
            self.device(description="More options").click()
            self.device.delay(2)
            self.device(text="Exit").click()
        else:
            self.back_to_home()

    def switch(self, status="Stop"):
        """Play  Stop
        """
        self.logger.info("switch FM to %s" % status)
        now = "Stop" if status == "Play" else "Play"
        self.device.delay()
        if self.device(description=now).exists:
            self.logger.info("FM status is status")
            return True
        else:
            self.device(description=status).click()
            self.device.delay(5)
            if self.device(description=now).wait.exists(timeout=2000):
                self.logger.info("switch FM to %s success" % status)
                return True
            else:
                self.logger.info("switch FM to %s failed" % status)
                self.save_fail_img()
                return True

    def scan_channel(self):
        self.logger.info("scan channel")
        self.device.delay()
        self.device(description="More options").click()
        self.device(text="Scan channels").click()
        if self.device(text="Cancel").wait.gone(timeout=20000):
            self.logger.info("scan channel success")
            return True
        else:
            self.logger.info("scan channel failed")
            self.save_fail_img()
            self.device(text="Cancel").click()
            self.exit()
            return False

    def switch_channel(self):
        self.logger.info("switch channel during play radio")
        self.enter()
        self.switch("Play")
        if self.channelSearch() :
            for i in range(5) :
                self.device(description = "Go to next").click()
                self.logger.debug("click %s times" %i)
                self.device.delay(5)
        else :
            self.save_fail_img()
            self.logger.debug("switch channel  failed")
            return False
        if self.device(resourceId = "com.tct.fmradio:id/menu_audio_mode").wait.exists(timeout = 2000) :
            self.logger.debug("change audio mode")
            self.device(resourceId = "com.tct.fmradio:id/menu_audio_mode").click()
            self.device.delay(5)
        self.logger.info("switch channel  success")
        return True
        
            
    def channelSearch(self):
        self.device.delay(3)
        self.device(description="More options").click()
        self.device.delay(1)
        self.device(text="Scan channels").click()
        #self.device(text="Searching").wait.gone(timeout = 10000)
        if self.device(resourceId="com.tct.fmradio:id/menu_channel_list").wait.exists(timeout=20000):
            self.device(resourceId="com.tct.fmradio:id/menu_channel_list").click()
            self.device.delay(2)
        else:
            self.logger.info('menu_channel_list not exists')
            return False
        channelCount = self.device(resourceId="com.tct.fmradio:id/channel_name").count
        if (channelCount > 0): 
            self.device.press.back() 
            self.logger.debug('channel exists')			
            return True
        else:
            self.device.press.back()
            self.logger.debug('channel is zero')			
            return False

    def play_fm(self):
        self.logger.info("play radio 30 min")
        self.enter()
        self.scan_channel()
        self.device.delay(1)
        if self.device(resourceId="com.tct.fmradio:id/play_stop").description == "Stop":
            self.logger.debug("FM working....")
            self.device.delay(1800000)
            if self.device(resourceId="com.tct.fmradio:id/play_stop").description == "Stop":
                self.logger.info("play radio 30 min success")
                self.exit()
                return True
            else:
                self.logger.info("play radio 30 min failed")
                self.save_fail_img()
                self.exit()
                return False
        else:
            self.logger.info("FM not working")
            self.save_fail_img()
            self.exit()
            return False


if __name__ == '__main__':
    a = FM("2cf8e42d", "fm")
    a.switch("Stop")