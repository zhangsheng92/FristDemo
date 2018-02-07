"""Browser library for scripts.
"""
import re
import sys
import os
import random
from common import *
from automator.uiautomator import Device


class Browser(Common):

    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self.appconfig.set_section("Browser")

    def enter(self):
        """Launch browser.
        """
        if self.device(resourceId="com.hawk.android.browser:id/forward_toolbar_id").wait.exists(timeout=self.timeout):
            return True
        self.logger.debug('enter browser')
        self.start_app("Chrome")
        self.device.delay(2)
        if self.device(resourceId="com.hawk.android.browser:id/forward_toolbar_id").wait.exists(timeout=self.timeout):
            self.logger.debug("enter browser success")
            return True
        return False

    def exit(self):
        """exit browser.
        """
        self.logger.debug('exit browser')
        if not self.device(packageName = "com.hawk.android.browser"):
            return True
        if self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").exists:
            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
            self.device.delay(1)
            self.device.swipe(1368,1730,100,1730, 10)
            self.device.delay(1)
            self.device(text="Quit").click()
            self.device.delay(1)
            self.device(text="EXIT").click()
            self.device.delay(1)
        if not self.device(packageName = "com.hawk.android.browser"):
            self.device.press.back()
            return True
        return False

    def home(self):
        '''back to homepage
        '''
        self.logger.info("back to homepage")
        for i in range(5):
            if self.device(text="Search or Type URL").wait.exists(timeout=2000):
                return
            self.device.press.back()
        else:
            self.logger.warning("Cannot back to homepage")

    def browser_webpage(self, website="www.wikipedia.org"):
        """browser webpage
        """
        self.logger.info("browser webpage %s" % website)
        if not self.device(text="Search or Type URL").exists:
            self.enter()
        self.device.delay(1)
        #self.device(resourceId="Search or Type URL").clear_text()
        #self.device.delay(1)
        self.device(text="Search or Type URL").click()
        self.device.delay(1)
        #self.device(text="Bookmarks").click()
        #self.device.delay(1)
        self.device(text="Search or Type URL").set_text(website)
        #self.device.set_text(website)
        self.device.delay(1)
        self.device.press.enter()
        self.device.delay(1)
        self.logger.debug('loading...')
        if not self.device(resourceId="com.hawk.android.browser:id/stop").wait.gone(timeout=30000):
            self.logger.debug("%s open fail!" % website)
            self.save_fail_img()
            return False
        else:
            self.logger.debug("%s load success!" % website)
            self.device.delay(2)
            return True

    def save_bookmark(self, page="https://m.baidu"):
        '''save current page to bookmark
        '''
        self.logger.debug("save %s to bookmark" % page)
        if self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").exists:
            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
            self.device.delay(1)
            self.device.swipe(100,1730,1368,1730, 10)
            self.device.delay(1)
            #self.device(text="Add Bookmark").click()
            #self.device.delay(1)
        step=[
            {"id":{"text":"Add Bookmark"}},
            {"id":{"resourceId":"com.hawk.android.browser:id/menu_toolbar_id"}},
            {"id":{"text":"Bookmark/History"}},
            {"id":{"text":"Bookmarks"}},
        ]
        UIParser.run(self, step)
        self.device.delay(2)
        if self.device(textStartsWith=page).exists:
            self.logger.debug("set %s to bookmark success" % page)
            return True
        else:
            self.save_fail_img()
            self.logger.error("set %s to bookmark failed" % page)
            return False


    def del_bookmark(self, page= "https://www.baidu"):
        '''delete bookmark -- page
        '''
        self.logger.debug("delete %s bookmark" % page)
        step=[
            {"id":{"resourceId":"com.hawk.android.browser:id/bookmark_item_more"}},
            {"id":{"text":"Clear"}},
            {"id":{"text":"CLEAR"}}
        ]
        UIParser.run(self, step)
        self.device.delay(2)
        if not self.device(textStartsWith=page).exists:
            self.logger.debug("delete %s bookmark success" % page)
            return True
        else:
            self.logger.error("delete %s bookmark failed" % page)
            self.save_fail_img()
            return False

    def clear_data(self):
        """clear data of browser
        """
        self.logger.debug('Clear browser data')
        if self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").exists:
            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
            self.device.delay(1)
            self.device.swipe(1368,1730,100,1730, 10)
            self.device.delay(1)
            self.device(text="Settings").click()
            self.device.delay(1)
            self.device(text="Clear data").click()
            self.device.delay(1)
            if self.device(text="Clear data").exists:
                self.device(text="CLEAR").click()
                self.logger.info("clear data complete")
                self.home()
            else:
                self.logger.info("clear data failed")
                self.home()


    def select_menu(self,menu_text):
        """enter node of menu
        """
        self.logger.debug('enter menu: '+ menu_text)
        if self.device(text = self.appconfig("bookmarks_title","Browser")).exists:
            return True
        self.device(description=self.appconfig("options","Browser")).click()
        if self.device(text=menu_text).wait.exists(timeout = self.timeout):
            self.device(text=menu_text).click()
        else:
            self.device(scrollable=True).scroll.vert.forward(steps=10)
            self.device(text=menu_text).click()
        self.device.delay(2)
        return True

    def select_bookmark(self, number):
        """load webpage from bookmark
        """
        self.logger.info("open bookmarks %d"%(number+1))
        #self.select_menu('Bookmarks')
        if self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").exists:
            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
            self.device.delay(1)
            self.device.swipe(100,1730,1368,1730, 10)
            self.device.delay(1)
            self.device(text="Bookmark/History").click()
            self.device.delay(1)
            self.device(text="Bookmarks").click()
            self.device.delay(1)
        bookmark = self.device(resourceId="com.hawk.android.browser:id/bookmark_list").child(className="android.widget.RelativeLayout" , index=number)
        bookmark.click()
        self.logger.debug('loading...')
        self.device.delay(2)
        if not self.device(resourceId="com.hawk.android.browser:id/stop").wait.gone(timeout=30000):
            self.logger.debug("Bookmark %s load failed!"%(number+1))
            self.save_fail_img()
            return False
        self.logger.debug("Bookmark %s load success!"%(number+1))
        return True

    def is_playing_streaming(self):
        self.device.delay(2)
        self.logger.info("click streaming start")
        self.device(description="a.3gp").click()
        self.device.delay(2)
        if self.device(text="Open with").exists:
            self.device(text="Video player").click()
            self.device(text="ALWAYS").click()
        self.device.delay(2)
        if self.device(packageName="com.tct.gallery3d").wait.exists(timeout=20000):
            self.logger.debug("The video is playing now")
            if self.device(text="OK").wait.exists(timeout=5000):
                self.device(text="OK").click()
            return True
        else:
            self.save_fail_img()
            return False

    def back_to_webpage(self, back_url):
        self.device.press.back()
        if self.device(resourceId="com.android.browser:id/progress").wait.gone(timeout=60000):
            url=self.device(className='android.widget.EditText',resourceId=self.appconfig.id("id_url","Browser")).get_text()
            if url==back_url:
                self.logger.info("back to %s success"%back_url)
                return True
        self.logger.info("back to %s failed"%back_url)
        self.save_fail_img()
        return False

    def navigation(self):
        bef_url= self.device(resourceId="com.hawk.android.browser:id/url").get_text()
        self.logger.debug("Before URL: %s" % bef_url)
        self.device.click(840, 1115)
        self.device.delay(2)
        if self.device(resourceId="com.hawk.android.browser:id/stop").wait.gone(timeout=60000):
            self.device.delay(2)
            af_url= self.device(resourceId="com.hawk.android.browser:id/url").get_text()
            self.logger.debug("After URL: %s" % af_url)
            if bef_url != af_url:
                self.logger.info("Navigation %s success."%af_url)
                self.device.delay(2)
                self.device.press.back()
                if self.device(resourceId="com.hawk.android.browser:id/stop").wait.gone(timeout=60000):
                    if self.device(resourceId="com.hawk.android.browser:id/url").get_text()==bef_url:
                        self.logger.info("back %s success"%bef_url)
                        self.device.delay(2)
                        return True
        self.logger.info("Navigation %s failed."%bef_url)
        self.save_fail_img()
        return False

    def del_download(self):
        self.logger.debug('Delete all download files!!!')
        #self.home()
        self.device.press.back()
        self.device.delay(2)
        if self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").exists:

            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
            self.device.delay(1)
            self.device.swipe(100,1730,1368,1730, 10)
            self.device.delay(1)
            self.device(text="Downloads").click()
            self.device.delay(1)
            self.device(text="Downloaded").click()
        else:
            self.logger.debug(">>>>>" + self.device.dump())
            self.device(resourceId="com.hawk.android.browser:id/menu_toolbar_id").click()
        for i in range(10):
            if self.device(text="No Downloaded file").wait.exists():
                self.logger.info("delete all download files success!!!")
                return True
            if self.device(resourceId="com.hawk.android.browser:id/apk_remove_btn").wait.exists():
                self.device(resourceId="com.hawk.android.browser:id/apk_remove_btn").click()
                self.device.delay(1)
        self.logger.debug("delete download files failed!!!")
        self.save_fail_img()
        return False

    def download(self, filetype):
        '''download file
        '''
        self.browser_webpage(self.appconfig(filetype, "Browser"))
        self.device.delay(1)
        if self.device(text="ALLOW DOWNLOAD").wait.exists():
            self.device(text="ALLOW DOWNLOAD").click()
        elif self.device(text="REPLACE FILE").wait.exists():
            self.device(text="REPLACE FILE").click()
            self.device.delay(1)
            self.device(text="ALLOW DOWNLOAD").click()
        self.device.open.notification()
        if self.device(text="Download complete.").wait.exists(timeout=30000):
                self.logger.info("download %s success" % filetype)
                return True
        '''if self.device(text="download").wait.exists() and self.device(text="No Downloads").wait.exists(timeout=30000):
            self.logger.info("download %s success"%filetype)
            self.device(text="Downloaded").click()
            self.device.delay(1)
            #self.del_download()
            return True'''
        self.logger.info("download %s failed"%filetype)
        self.save_fail_img()
        self.device.press.back()
        return False


    def play_file(self, filetype,loop=0):
        self.logger.info("play %s?"%filetype)
        self.device.delay(1)
        #self.device(resourceId="com.hawk.android.browser:id/downloads_recycler").child(index=0).click()
        self.device(text="Download complete.").click()
        if filetype == "Music":
            if loop == 0:
                if self.device(text="Open with").exists:
                    self.device(text="Music").click()
                    self.device(text="ALWAYS").click()
            if self.device(packageName="com.google.android.music").wait.exists(timeout=2000):
                self.logger.debug("The music is playing now")
                self.device.press.back()
                return True
        else:
            if loop == 0:
                if self.device(text="Open with").exists:
                    self.device(text="Video player").click()
                    self.device(text="ALWAYS").click()
            self.device.delay()
            if self.device(packageName="com.tct.gallery3d").wait.exists(timeout=2000):
                self.logger.debug("The video is playing now")
                self.device.press.back()
                return True
        #self.device.press.back()
        self.save_fail_img()
        self.logger.info("%s not playing"% filetype)
        return False


    def open_webpage(self,times=1):
        self.logger.debug("Open a webpage %d times." % times)
        for index in range(times):
            try:
                self.enter()
                self.clear_data()
                if self.browser_webpage() and self.save_bookmark() and self.del_bookmark():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(index+1))
            except Exception,e:
                self.logger.error(e)
                self.save_fail_img()
            finally:
                self.home()
        self.exit()
        self.logger.debug("Open a webpage %d times complete." % times)

    def open_bookmark(self,times = 1):
        self.logger.debug("Open bookmarks %d times." % times)
        self.enter()
        self.clear_data()
        for index in range(times):
            try:
                if self.select_bookmark(random.randint(0, 4)):
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (index+1))
            except Exception,e:
                self.logger.error(e)
                self.save_fail_img()
                self.enter()
            finally:
                self.home()
        self.exit()
        self.logger.debug("Open bookmarks %d times." % times)

    def play_streaming(self,times = 1):
        self.logger.debug("Play Streaming  %d times"%times)
        self.enter()
        self.clear_data()
        self.browser_webpage(self.appconfig("Streaming","Browser"))
        for loop in range(times):
            try:
                if self.is_playing_streaming() and self.back_to_webpage(self.appconfig("Streaming","Browser").split(r"//")[1]):
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
            except Exception, e:
                self.logger.error(e)
                self.save_fail_img()
        self.exit()
        self.logger.debug("Play Streaming %d times complete"%times)


    def webnavigation(self, times=1):
        self.logger.debug('web Navigation %d Times.' % (times))
        self.enter()
        home_url=self.device(resourceId="com.android.browser:id/url").get_text()
        self.logger.debug("Home URL: %s" % home_url)
        self.clear_data()
        for index in range(times):
            try:
                if self.browser_webpage() and self.navigation() and self.back_to_webpage(home_url):
                     self.suc_times += 1
                     self.logger.info("Trace Success Loop "+ str(index+1))
            except Exception,e:
                self.logger.error(e)
                self.save_fail_img()
            finally:
                self.home()
        self.exit()
        self.logger.debug('web Navigation %d Times complete.' % (times))

    def download_text_picture(self, filetype, times=1):
        '''download text / picture
        '''
        self.logger.debug('Download %s %d Times' %(filetype, times))
        self.enter()
        self.clear_data()
        for loop in range(times):
            try:
                if self.download(filetype, random_name(loop)) and self.del_download():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (loop+1))
            except Exception,e:
                self.logger.error(e)
                self.save_fail_img()
            finally:
                self.device.press.back()
        self.exit()
        self.logger.info("download %s Test complete"%filetype)

    def download_play_audio_vedio(self, filetype, times=1):
        self.logger.debug('Download and play %s %d Times' % (filetype, times))
        self.enter()
        self.clear_data()
        for loop in range(times):
            try:
                if self.download(filetype, random_name(loop)) and self.play_file(filetype) and self.del_download():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (loop+1))
                else: self.clear_notification()
            except Exception,e:
                self.logger.error(e)
                self.save_fail_img()
            finally:
                self.device.press.back()
        self.exit()
        self.logger.info("Download and play %s Test Completed"%filetype)



if __name__ == '__main__':
    a = Browser("2cd4e62e","Browser")
    a.device.dump()
#     a.open_webpage(1)#1
#     a.open_bookmark(1)#2
#     a.download_text_picture("Text",1)#3
#     a.download_play_audio_vedio("Music",1)#4
#     a.download_text_picture("Picture",1)#5
    a.download_play_audio_vedio("Video",1)#6
#     a.webnavigation(1)#8
#     a.play_streaming()#7
#     a.play_file("Video")
#     a.setup()
#     a.play_file("1")


