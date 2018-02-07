# -*- coding: UTF-8 -*-
"""multi tasking library for scripts.
"""

from common import *


class MultiTask(Common):

    def start(self):
        """case precondition, start some apps
        """
        self.logger.debug("Start Some activities")
        self.start_activity("com.android.dialer" , "com.android.dialer.DialtactsActivity")
        self.start_activity("com.android.mms" , "com.android.mms.ui.ConversationList")
        self.start_activity("com.android.dialer" , "com.android.dialer.DialtactsActivity")
        self.start_activity("com.tct.camera" , "com.android.camera.CameraLauncher")
        self.start_activity("com.tct.email" ,"com.tct.email.activity.Welcome")
        self.start_activity("com.alcatel.music5" , "com.alcatel.music5.activities.MusicPlayerActivity")
        self.device.press.home()

    def back_end_call(self):
        """back to call page and end call
        """
        self.logger.info("back to the call and end the call")
        self.device.open.notification()
        if self.device(text="Ongoing call").wait.exists():
            self.device(text="Ongoing call").click()
            if self.device(description='End').wait.exists(timeout=2000):
                self.logger.info("back to call success")
                self.device(description="End").click()
                self.device.delay(1)
                if not self.device(description='End').exists:
                    self.logger.info("end call success")
                    return True
                else:
                    self.logger.info("end call failed")
                    self.save_fail_img()
                    return False
        else:
            self.logger.info("Call has ended")
            self.device.press.home()
            return True
            
    def interaction(self, times=6):
        """switch applications page
        """
        self.logger.debug("switch applications %d times" % times)
        self.device.press.home()
        self.device.delay(2)
        for loop in range(1, times + 1):
            self.device.press.recent()
            self.device.delay(1)
            for i in range(2):
                self.device.swipe(660,200,660,1400, 10)
            self.device.delay(1)
            self.device.click(600, 355)
            self.device.delay()
            if not self.device(resourceId='com.android.systemui:id/task_view_thumbnail').exists:
                self.logger.debug("Switch applications loop %d success" % loop)
            else:
                self.logger.info("Switch applications loop %d failed" % loop)
                self.save_fail_img()
                return False
        self.device.press.home()
        self.logger.debug("switch applications %d times success" % times)
        return True
        
#if __name__ == '__main__':
    #a=MultiTask("80c08ac6","task")
    # a.interaction(6)
    #a.back_end_call()
    # a.device.swipe(660,200,660,2000, 10)
    # a.interaction(6)