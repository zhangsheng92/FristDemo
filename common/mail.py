# -*- coding: utf-8 -*-
"""Email library """

from common import Common, UIParser


class Email(Common):
    def enter(self):
        """Launch email by StartActivity.
        """
        self.logger.debug("Launch email.")
        if self.device(description=self.appconfig("navigation", "Email"),packageName="com.tct.email").wait.exists(timeout=self.timeout):
            return True
        self.start_app("Email")
        return self.device(description=self.appconfig("navigation", "Email"),packageName="com.tct.email").wait.exists(timeout=self.timeout)

    def enter_box(self, box):
        """enter the box you want  
        arg: (str)box --text of the box
        """
        self.logger.debug('enter the box: %s', box)
        if not self.device(packageName="com.tct.email").exists:
            self.enter()
        if self.device(text=box).exists:
            self.device(text=box).click()
        if self.device(text=box, index=2).exists:
            return True
        for i in range(3):
            if self.device(description="Open navigation drawer").wait.exists(timeout=2000):
                break
            else:
                self.device.press.back()
                self.device.delay(1)
        self.device(description="Open navigation drawer").click()
        self.device(text=box).click.wait(timeout=2000)
        if self.device(text=box, index=2).wait.exists():
            return True
        self.logger.warning("Cannot change to box: %s" % box)
        self.save_fail_img()
        return False

    def send_mail(self, send_type, att_flag, address=None):
        """send a email
        arg: send_type(str) forward or reply email
             address(str) email address you want to send
             att_flag(boolean) whether to send with attachments
        """
        if self.device(description='Dismiss tip').exists:
            self.device(description='Dismiss tip').click()
            self.device.delay(1)
        self.logger.debug('create an email')
        if att_flag:
            self.device(resourceId="com.tct.email:id/conversation_list_view").child(
                className='android.widget.FrameLayout', index=3).click()
        else:
            self.device(resourceId="com.tct.email:id/conversation_list_view").child(
                className='android.widget.FrameLayout', index=2).click()
        if self.device(resourceId="com.tct.email:id/overflow").wait.exists(timeout=5000):
            self.device(resourceId="com.tct.email:id/overflow").click()
            self.device(text=send_type).click()
            self.device.delay(2)
            if send_type == "Forward":
                self.device(resourceId = "com.tct.email:id/to").set_text(address)
            else:
                self.device(text='Compose email').set_text("Reply email. go spurs go.")
            self.device(description='Send').click.wait(timeout=2000)
            self.device.delay()
            self.logger.debug('email sending...')
            self.device.press.back()
            return self.verify_sending()
        else:
            self.logger.warning('Cannot open an email')
            self.save_fail_img()
            return False

    def del_mail(self, box):
        """delete all email of the box  
        arg: (str)box --text bof the box
        """
        self.logger.debug('delete the mail of %s' % box)
        if not self.device(text=box).exists:
            self.device(description=self.appconfig("navigation", "Email")).click()
            self.device(text=box).click()
            self.device.delay(2)
        if not self.device(resourceId="com.tct.email:id/conversation_list_view").child(index=2).exists:
            self.logger.info("the %s box no mails" % box)
            self.device.press.back()
            return True
        if box == "Trash":
            if self.device(text="EMPTY TRASH").exists:
                self.device(text="EMPTY TRASH").click()
                self.device.delay(1)
                self.device(text="DELETE").click()
                self.device.delay(1)
                return True
            '''if self.device(resourceId="com.tct.email:id/empty_text").wait.exists(timeout=5000):
                self.logger.info("delete the mail of Trash success")'''

        elif box == "Drafts" or box == "Sent":
            if self.device(text="There is no mail here.").exists:
                self.logger.info("no mails in drafts box")
                return True
            x, y = self.device(resourceId="com.tct.email:id/conversation_list_view").child(index=2).get_location()
            self.device.swipe(x, y, x + 1, y + 1, 200)
            if self.device(resourceId="com.tct.email:id/select_all").exists:
                self.device(resourceId="com.tct.email:id/select_all").click()
            self.device(resourceId="com.tct.email:id/star_toggle").click()
            if self.device(text="OK").wait.exists():
                self.device(text="OK").click()
            if self.device(text="There is no mail here.").wait.exists(timeout=5000):
                self.logger.info("delete the mail of drafts success")
                self.device.press.back()
                return True
        else:
            self.device.delay(1)
            for i in range(5):
                self.device.swipe(150, 660, 1200, 660, 50)  # delete the first mail from box list
                self.device.delay(1)
                if self.device(text="There is no mail here.").wait.exists(timeout=2000):
                    self.logger.info("delete the mail of %s success" % box)
                    self.device.press.back()
                    return True
        self.device.delay(2)
        self.device.press.back()
        self.logger.info("delete the mail of %s failed" % box)
        self.save_fail_img()
        return False

    def create_draft(self, address, loop=0):
        """ save a draft mail
        arg: address(str) draft mail address
             loop(int) draft mail content
        """
        self.device(resourceId="com.tct.email:id/compose_button").click.wait()
        self.device(resourceId="com.tct.email:id/to").set_text(address)
        self.device.press.enter()
        self.device(text="Subject").set_text("Stability Test %d" % loop)
        self.device.press.enter()
        self.device(text="Compose email").set_text("Stability Test. Go spurs go.")

        # you can get attach file to save draft mail
        # self.device(description="Attach file").click.wait()
        # self.logger.info("add test_picture.jpg attach from internal storage")
        # self.device.delay()
        # if not self.device(text="Internal storage", index=1).exists:
        #     if not self.device(text="Open from").exists:
        #         self.device(description="Show roots").click()
        #     self.device(text="Internal storage").click.wait()
        # if self.device(scrollable=True):
        #     self.device(scrollable=True).scroll.vert.toEnd()
        # if self.device(text="test_picture.jpg").wait.exists(timeout=2000):
        #     self.device(text="test_picture.jpg").click()
        # else:
        #     self.logger.info("not test_picture.jpg  File")
        #     self.device.press.back()

        self.device(description="More options").click()
        self.device(text="Save draft").click()
        self.device.press.back()
        self.enter_box("Drafts")
        if self.device(resourceId="com.tct.email:id/conversation_list_view").child(index=2).exists:
            self.logger.info("Create draft Stability Test %d success" % loop)
            return True
        else:
            self.logger.info("Create draft Stability Test %d failed" % loop)
            self.save_fail_img()
            return False

    def send_draft(self, loop):
        """send a draft mail
        """
        self.logger.info("send draft Stability Test %d" % loop)
        self.device(resourceId="com.tct.email:id/conversation_list_view").child(index=2).click()
        if self.device(text="Stability Test %d " % loop).wait.exists(timeout=2000):
            self.logger.info("enter draft Stability Test %d success" % loop)
            self.device(description="Edit").click.wait(timeout=2000)
            self.device(description="Send").click.wait(timeout=2000)
            self.device.press.back()
            self.device.delay(2)
            return self.verify_sending()
        else:
            self.logger.info("enter draft Stability Test %d failed" % loop)
            self.save_fail_img()
            return False

    def verify_sending(self):
        """Validation email sent successfully in 3 minutes
        """
        self.logger.debug('Verify email sending !!!')
        self.enter_box("Outbox")
        if self.device(text="There is no mail here.").wait.exists(timeout=180000):
            self.logger.debug('email send !!!')
            self.device.press.back()
            return True
        else:
            self.logger.debug('email send fail in 3 min!!!')
            self.save_fail_img()
            self.del_mail("Outbox")
            self.del_mail("Trash")
            return False
            
            
    def refesh_email(self):
        """refesh email in sent.

        author: tao.wu   585  610
        """       
        self.logger.debug("Check email status")
        if not self.enter_box("Sent"):
            return False
        self.device.swipe(585,610,585,1270)	
        if self.device(text="1 unsent in Outbox").exists:
            self.enter_box("Outbox")
            self.device.delay(2)
            self.device.swipe(585,610,585,1270)
            if not self.device(resourceId="com.tct.email:id/empty_view").exists:
                self.device.swipe(585,610,585,1270)
        self.enter_box("Sent")
            
            
    def get_email_num(self):
        """get number of email in the mailbox.

        return the number of email in the mail box
        author: Zhx
        """
        self.logger.warning("---------------------------")
        if self.device(resourceId="com.tct.email:id/empty_text").exists:
            email_num = 0
        else:
            list_num = self.device(resourceId="com.tct.email:id/conversation_list_view").getChildCount()
            self.logger.warning(str(list_num)+"---------------------------")
            if self.device(resourceId="com.tct.email:id/load_more").exists or \
                    self.device(resourceId="com.tct.email:id/loading").exists:
                email_num = list_num - 3
            else:
                email_num = list_num - 2
        self.logger.debug("Number of email is: " + str(email_num))
        return email_num
        
        
    def select_mail(self, flag):
        """select the mail in list by index.

        argv: (int)index -- mail order in list. Start from 0.
        author: Zhx
        """
        self.logger.debug("Select the email----------------------------")
        inbox_num = 2#self.get_email_num()
        if inbox_num > 2 and flag == 1:
            Index = inbox_num - 1
        elif inbox_num > 2 and flag == 0:
            Index = inbox_num - 2
        elif inbox_num == 2:
            Index = flag
        else:
            self.logger.warning("No email exist!")
            return False
        self.device(className="android.widget.ListView").child(className="android.widget.FrameLayout", instance=Index+1).click()
        self.device.delay(1)
        if self.device(resourceId="com.tct.email:id/overflow").wait.exists(timeout=3000):
            return True
        else:
            self.logger.warning("Cannot enter the select mail!")
            return False



#if __name__ == '__main__':
    #a = Email("80c08ac6", "Email")
    #a.enter()
    # a.send_mail("Reply", True, "jia.huang@tcl.com")
    # a.del_mail("Sent")
    # a.del_mail('Trash')
    # a.enter_box("Inbox")
    #a.create_draft("jia.huang@tcl.com", 1)
    #a.send_draft(1)
    #a.del_mail('Sent')
    #a.del_mail('Trash')
    #a.enter_box("Inbox")