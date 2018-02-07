"""Recorder library for scripts.
"""

from common import *


class Recorder(Common):
    """Provide common functions involved Sound Recorder."""

    def enter(self):
        """Launch Recorder by StartActivity.
        """
        self.logger.debug('enter Soundrecorder')
        if self.device(resourceId=self.appconfig.id("id_record", "Recorder")).wait.exists(timeout=self.timeout):
            return True
        self.start_app(self.appconfig("name", "Recorder"))
        while self.device(text="ALLOW").wait.exists(timeout=3000):
            self.device(text="ALLOW").click()
            self.device.delay(2)
        return self.device(resourceId=self.appconfig.id("id_record", "Recorder")).wait.exists(timeout=self.timeout)

    def back_main_app(self):
        self.logger.debug("Back to main app")
        for i in range(5):
            if self.device(resourceId=self.appconfig.id("id_record", "Recorder")).exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to main app")

    def get_storage_num(self):
        return self.get_file_num(self.appconfig("storage", "Recorder"), ".amr") + self.get_file_num(
            self.appconfig("storage", "Recorder"), ".m4a") + self.get_file_num(self.appconfig("storage", "Recorder"),
                                                                               ".3gpp")

    def clear(self):
        self.logger.debug('clear audio')
        self.device(resourceId="com.tct.soundrecorder:id/file_list").click()
        for i in range(10):
            if not self.device(description="File option menu").exists:
                self.logger.info("not audio exists")
                break
            self.device(description="File option menu").click()
            self.device(text=self.appconfig("delete", "Recorder")).click()
            self.device(text="DELETE").click()
        self.back_main_app()

    def record(self, filename, duration=5):
        """record audio several seconds.
        argv: (int)duration -- recording time
        """
        self.logger.debug("Record audio %s %s seconds." % (filename, duration))
        file_num = self.get_storage_num()
        self.device(resourceId=self.appconfig.id("id_start", "Recorder")).click()
        if not self.device(resourceId=self.appconfig.id("id_timerView", "Recorder")).wait.exists(timeout=self.timeout):
            self.logger.warning("Fail to start recording!")
            return False
        self.device.delay(duration)
        self.logger.debug("Stop recording audio")
        self.device(text="SAVE").click()
        self.device(resourceId="com.tct.soundrecorder:id/edit_text").set_text(filename)
        self.device(text="SAVE").click.wait(timeout=2000)
        if file_num >= self.get_storage_num():
            self.logger.warning("Save audio fail!!!")
            self.save_fail_img()
            return False
        else:
            self.logger.debug("Save audio success!!!")
            return True

    def enter_audio_list(self):
        """Enter audio file list.
        """
        self.logger.debug("Enter Audio List")
        if self.device(resourceId=self.appconfig.id("id_filelist", "Recorder")).wait.exists(timeout=self.timeout):
            self.device(resourceId=self.appconfig.id("id_filelist", "Recorder")).click()
        if not self.device(text=self.appconfig("filelist_title", "Recorder")).wait.exists(timeout=self.timeout):
            self.logger.warning("Cannot Enter file list")
            return False
        return True

    def play(self, name, duration=10):
        """touch audio according to index.
        argv: (int)index -- file order in list
        """
        self.logger.info("play audio %s " % name)
        if self.device(text=name).wait.exists(timeout=2000):
            self.device(text=name).click()
            if self.device(resourceId=self.appconfig.id("id_statebar", "Recorder")).wait.exists(timeout=self.timeout):
                self.logger.debug("audio %s Start Playing..." % name)
                self.device.delay(duration)
                return True
            self.logger.info("Cannot play audio %s." % name)
            self.save_fail_img()
            return False
        else:
            self.logger.info("audio %s not exists" % name)
            self.save_fail_img()
            return False

    def delete(self, name):
        """delete audio

        argv: (int)index -- file order in list. Default is 0.
        """
        self.logger.debug("Delete Audio %s." % name)
        self.device.delay(2)
        audio_num = self.get_storage_num()
        if self.device(text=name).exists:
            self.device(text=name).sibling(description="File option menu").click()
            self.device(text=self.appconfig("delete", "Recorder")).click()
            self.device(text="DELETE").click()
            self.device.delay(2)
            if audio_num <= self.get_storage_num():
                self.logger.warning("Delete audio %s failed." % name)
                self.save_fail_img()
                return False
            else:
                self.logger.warning("Delete audio %s success." % name)
                self.back_main_app()
                return True
        else:
            self.logger.info("audio %s not exists" % name)
            self.save_fail_img()
            return False


if __name__ == '__main__':
    a = Recorder("80c08ac6", "Recorder")
    a.enter()
    a.record("111")
    a.play("111")
    a.delete("111")
    a.clear()