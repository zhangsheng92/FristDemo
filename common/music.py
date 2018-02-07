"""Camera library for scripts.
"""

from common import *


class Music(Common):

    def enter(self):
        """Launch music by StartActivity.
        """
        self.logger.debug('enter music')
        if self.device(packageName="com.alcatel.music5").wait.exists(timeout=5000):
            return True
        self.start_app("Music")
        while self.device(text="ALLOW").wait.exists(timeout=3000):
            self.device(text="ALLOW").click()
            self.device.delay(2)
        return self.device(packageName="com.alcatel.music5").wait.exists(timeout=5000)

    def play_music(self):
        self.logger.debug(" Start music player.")
        #self.start_app("Play Music", False)
        self.enter()
        if self.device(text="SHUFFLE ALL").exists:
            self.device(text="SHUFFLE ALL").click()
            self.device.delay(2)
        music = self.device(resourceId="com.alcatel.music5:id/title_text_view").get_text()
        self.logger.info("start play music %s" % music)
        #self.device(resourceId="com.alcatel.music5:id/item_recycler_parent_view", index=index + 3).click()
        self.device.delay(1)
        if self.is_playing_music():
            self.device.delay(5)
            self.logger.info("play music %s success" % music)
            return True
        self.logger.info("play music %s failed" % music)
        self.save_fail_img()
        return False

    def close_music(self):
        self.back_to_home()
        self.logger.info("closed music")
        if self.is_playing_music():
            self.device.open.notification()
            self.device(resourceId = "com.alcatel.music5:id/track_play_pause_image_btn").click.wait(timeout=2000)
            if self.device(resourceId="com.android.systemui:id/dismiss_text").wait.exists():
                self.device(resourceId="com.android.systemui:id/dismiss_text").click()
            else:
                self.device.press.home()
            if not self.is_playing_music():
                self.logger.info("closed music success")
                return True
            self.logger.info("closed music failed")
            return False
        else:
            self.logger.info("music is not playing")
            return True


if __name__ == '__main__':
    a = Music("2cd0e633", "Music")
    print a.device.dump(r"c:\recorder.xml")