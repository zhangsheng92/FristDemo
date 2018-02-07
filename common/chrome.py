# -*- coding: utf-8 -*-

from common import *

class Chrome(Common):

    def enter(self):
        """Launch Chrome.
        """
        self.logger.debug('enter Chrome')
        if self.device(resourceId=self.appconfig.id("id_location_bar", "Chrome")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Chrome")
        if self.device(resourceId="com.android.chrome:id/terms_accept").wait.exists(timeout=5000):
            self.device(resourceId="com.android.chrome:id/terms_accept").click()
            if self.device(resourceId="com.android.chrome:id/positive_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.chrome:id/positive_button").click()
            if self.device(text="No thanks").wait.exists(timeout=5000):
                self.device(text="No thanks").click()

    def home(self):
        """back to home page
        """
        self.logger.debug('Back Chrome')
        for i in range(5):
            if self.device(resourceId="com.android.chrome:id/tab_switcher_button").wait.exists(timeout=2000):
                self.device(resourceId="com.android.chrome:id/tab_switcher_button").click()
                self.device.delay(2)
                #self.device(description="More options").click.wait(timeout=2000)
                #self.device(text="Close all tabs").click.wait(timeout=2000)
                self.device(resourceId="com.android.chrome:id/new_tab_button").click()
                return
            self.device.press.back()
        else:
            self.logger.warning("Cannot back to Chrome")

    def exit(self):
        """exit chrome
        """
        self.logger.debug('Exit chrome')
        for i in range(3):
            if self.device(resourceId="com.android.chrome:id/tab_switcher_button").wait.exists(timeout=2000):
                self.device(resourceId="com.android.chrome:id/tab_switcher_button").click()
                self.device(description="More options").click.wait(timeout=2000)
                self.device(text="Close all tabs").click.wait(timeout=2000)
                #self.device(resourceId="com.android.chrome:id/new_tab_button").click()
                self.device.press.back()
                return True
            self.device.press.back()
        self.device.press.back()
        self.device.press.home()

    def browser_webpage(self, website="www.wikipedia.org"):
        """browser web page
        arg：website(str) the web page address
        """
        self.logger.info("browser webpage %s" % website)
        if not self.enter() :
            self.enter()
        self.device.delay(2)
        if self.device(resourceId = "com.android.chrome:id/url_bar").wait.exists(timeout = 3000) :
            self.device(resourceId = "com.android.chrome:id/url_bar").set_text(website)
        if self.device(text = "Search or type URL").wait.exists(timeout = 3000) :
            self.device(text = "Search or type URL").set_text(website)
        self.device.press.enter()
        self.device.delay(2)
        self.logger.debug('loading...')
        if not self.device(resourceId=self.appconfig.id("id_progress", "Chrome")).wait.gone(timeout=30000):
            self.logger.debug("%s open time out!" % website)
            self.save_fail_img()
            return False
        else:
            self.logger.debug("%s load success!" % website)
            self.device.delay(2)
            return True

    def save_bookmark(self, page=u"百度一下"):
        """save current page to bookmark
        arg：page(str) the bookmark name
        """
        self.logger.debug("save %s to bookmark" % page)
        self.device(description=self.appconfig("options", "Chrome")).click()
        if self.device(description="Edit bookmark").wait.exists(timeout=1000):
            self.device(description="Edit bookmark").click()
            self.device(description="Delete bookmarks").click.wait(timeout=2000)
            self.device(description=self.appconfig("options", "Chrome")).click.wait(timeout=2000)
        self.device(description="Bookmark this page").click()
        self.device(description=self.appconfig("options", "Chrome")).click.wait(timeout=2000)
        self.device(text="Bookmarks").click()
        if self.device(text=page).wait.exists(timeout=2000):
            self.logger.debug("set %s to bookmark success" % page)
            return True
        else:
            self.save_fail_img()
            self.logger.error("set %s to bookmark failed" % page)
            return False

    def del_bookmark(self, page=u"百度一下"):
        """delete bookmark
        arg：page(str) the bookmark name
        """
        self.logger.debug("delete %s bookmark" % page)
        step = [
            {"id": {"text": page}, "action": {"type": "long_click"}},
            {"id": {"description": "Delete bookmarks"}},
        ]
        UIParser.run(self, step)
        self.device.delay(2)
        if not self.device(text=page).exists:
            self.logger.debug("delete %s bookmark success" % page)
            return True
        else:
            self.logger.error("delete %s bookmark failed" % page)
            self.save_fail_img()
            return False

    def clear_data(self):
        """clear data of chrome
        """
        self.logger.debug('Clear browser data')
        self.device(description = self.appconfig("options", "Chrome")).click()
        self.device.delay(1)
        self.device(text = "History").click()
        self.device.delay(1)
        self.device.click(370 , 1250)
        self.device.delay(1)
        self.device(text = "CLEAR DATA").click()
        if self.device(description="History").wait.exists(timeout=2000):
            self.logger.info("clear data success")
            self.home()
            return True
        self.logger.info("clear data failed")
        self.home()

    def select_bookmark(self, number):
        """select an bookmark and open
        arg: number(int) which one bookmark
        """
        self.logger.info("open bookmarks %d" % (number + 1))
        self.device(description=self.appconfig("options", "Chrome")).click.wait(timeout=2000)
        self.device(text="Bookmarks").click.wait(timeout=2000)
        # bookmark = self.device(resourceId="com.android.chrome:id/eb_items_container").child(index=number).child(
        #     index=1).child(index=0).get_text()
        # self.logger.info("the bookmark is %s" % bookmark)
        self.logger.info("open bookmark %d"% (number + 1))
        #self.device(resourceId="com.android.chrome:id/bookmark_items_container").child(index=number).click()
        self.device(resourceId="com.android.chrome:id/bookmark_items_container").child(
                className='android.widget.FrameLayout', index=number).click()
        self.logger.debug('loading...')
        self.device.delay(2)
        if not self.device(resourceId=self.appconfig.id("id_progress", "Chrome")).wait.gone(timeout=30000):
            self.logger.debug("open bookmark %d failed"% (number + 1))
            self.save_fail_img()
            return False
        self.logger.debug("open bookmark %d success"% (number + 1))
        return True

    def back_to_webpage(self, back_url):
        self.device.press.back()
        if self.device(resourceId=self.appconfig.id("id_progress", "Chrome")).wait.gone(timeout=60000):
            url = self.device(resourceId="com.android.chrome:id/url_bar").get_text()
            if back_url in url:
                self.logger.info("back to %s success" % back_url)
                return True
        self.logger.info("back to %s failed" % back_url)
        self.save_fail_img()
        return False

    def navigation(self):
        bef_url = self.device(resourceId="com.android.chrome:id/url_bar").get_text()
        self.logger.debug("Before URL: %s" % bef_url)
        if self.device(description="登录").exists:
            self.device(description="登录").click()
        else:
            self.device.click(840, 1150)  # the "新闻" location
        self.device.delay(2)
        if self.device(resourceId=self.appconfig.id("id_progress", "Chrome")).wait.gone(timeout=60000):
            self.device.delay(2)
            af_url = self.device(resourceId="com.android.chrome:id/url_bar").get_text()
            self.logger.debug("After URL: %s" % af_url)
            if bef_url != af_url:
                self.logger.info("Navigation %s success." % af_url)
                return True
                '''if self.back_to_webpage(bef_url):
                    self.logger.info("back to chrome home")
                    self.device.press.back()
                    if self.device(text="Recent tabs").wait.exists():
                        self.logger.info("back to chrome home success")
                        return True
                    else:
                        self.logger.info("back to chrome failed")
                        self.save_fail_img()
                        return False
                else:
                    return False'''
        self.logger.info("Navigation %s failed." % bef_url)
        self.save_fail_img()
        return False

    def del_download(self):
        self.logger.debug('Delete all download files') 
        self.start_app("Downloads")
        if self.device(text = "No items").wait.exists(timeout = 2000):
            self.logger.info("no file exists")
            self.device.press.back()
            return True
        x, y = self.device(resourceId="com.android.documentsui:id/dir_list").child(index=0).get_location()
        self.device.swipe(x, y, x + 1, y + 1, 200)
        self.device(description="More options").click()
        self.device(text="Select all").click()
        self.device(resourceId = "com.android.documentsui:id/menu_sort").click()
        self.device(text="OK").click()
        if self.device(text = "No items").wait.exists(timeout = 2000):
            self.logger.info("delete all download files success!!!")
            self.back_to_home()
            return True
        self.logger.debug("delete download failed!!!")
        self.back_to_home()
        return False

    def download(self, filetype):
        '''download file
        '''
        self.logger.info("download %s" % filetype)
        self.browser_webpage(self.appconfig(filetype, "Chrome"))
        if self.device(text='In progress').wait.gone(timeout=30000):
            if self.device(text="REPLACE FILE").wait.exists():
                self.device(text="REPLACE FILE").click()
            self.device.open.notification()
            if self.device(text="Download complete.").wait.exists(timeout=30000):
                self.logger.info("download %s success" % filetype)
                return True
        self.logger.info("download %s failed" % filetype)
        self.save_fail_img()
        self.device.press.back()
        return False

    def play_file(self, filetype):
        self.logger.info("play %s" % filetype)
        self.device.delay()
        if filetype == "Audio":
            if self.device(textContains="Open with").exists:
                self.device(textContains="Music").click()
                self.device(text="JUST ONCE").click()
                self.device.delay(15)
            #if self.is_playing_music():
            if self.device(packageName="com.alcatel.music5").wait.exists(timeout=2000):
                self.logger.debug("The music is playing now")
                self.device.press.back()
                return True
        else:
            if self.device(textContains="Open with").exists:
                self.device(textContains="Video player").click()
                self.device(text="JUST ONCE").click()
                self.device.delay(5)
            if self.is_playing_video():
                self.device.press.back()
                return True
        self.device.press.back()
        self.logger.info("%s not playing" % filetype)
        self.save_fail_img()
        return False
        
    def open_links(self):
        """Open URL in id/url then jump to the page.


        author: Zhx
        """
        self.logger.debug("Open a link")
        temp_url = self.device(resourceId="com.android.chrome:id/url_bar").get_text()
        self.device.click(200,700)
        self.device.delay(3)
        if self.device(text=temp_url).wait.exists(timeout=8000):
            return False
        else:
            self.logger.debug("open links success")
            return True


#if __name__ == '__main__':
    #a = Chrome("80c08ac6", "Browser")
    # a.enter()
    #a.del_download()
    # a.download("Video")
    # a.play_file("Video")
    # a.clear_notification()
    # a.navigation()
    # a.back_to_webpage()
    # a.home()
    # a.exit()
    # home_url = a.device(resourceId="com.android.chrome:id/url_bar").get_text()
    # a.browser_webpage("wap.sogou.com")
    # a.navigation()
    # a.back_to_webpage(home_url)
    # a.download("Text")
    # a.play_file("Music")
    # a.download_text_picture("Text", 1)
    # a.download_play_audio_vedio("Music", 2)
    # a.download_text_picture("Picture",2)#5
    # a.download_play_audio_vedio("Video", 2)






