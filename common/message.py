# -*- coding: utf-8 -*-
"""message library for scripts.
"""
from common import *
from music import Music


class Message(Common):
    def __init__(self, device, log_name, sdevice=None):
        Common.__init__(self, device, log_name, sdevice)
        self.music = Music(self.device, "msg_music")
        self.appconfig.set_section("Message")
        self.msgs = {'MMS': "2", 'SMS': "1"}

    def enter(self):
        """Launch messaging.
        """
        self.logger.debug("enter Message")
        if self.device(resourceId="com.android.mms:id/floating_action_button").wait.exists(timeout=2000):
            return True
        self.start_app("Messaging")
        return self.device(resourceId="com.android.mms:id/floating_action_button").wait.exists(timeout=2000)

    def back_to_message(self):
        self.logger.debug("Back to messaging")
        for i in range(5):
            if self.device(description="add new message").exists and \
                    self.device(text="Messaging").exists:
                return True
            else:
                self.device.press.back()
                self.device.delay(1)
        self.logger.warning("Cannot back to messaging")
        return False
            
            
    def enter_pre_msg(self):
        """Enter the precondition message.

        author: Zhx
        """
        if self.device(description="add new message").wait.exists(timeout=5000) and \
                self.get_sms_num() >= 4:
            self.logger.debug("Already in the precondition messaging")
            return True
        else:
            if self.enter():
                self.device.delay(1)
                if self.device(description="add new message").wait.exists(timeout=5000) and \
                        self.get_sms_num() >= 4:
                    return True
                else:
                    self.logger.warning("Cannot enter the precondition messaging!")
                    return False
                    

    def s_send_msg(self, loop=0):
        """s-device send message to m-device
        """
        contentm = "Message test loop %d" % (loop + 1)
        self.logger.info("s-device send %s to m-device" % contentm)
        data = self.sdevice.server.adb.shell("am start -a android.intent.action.SENDTO -d sms:%s" % self.mdevice_msg)
        if data.find("Error") > -1:
            self.logger.error("Fail to send a sms to m-device.")
            return False
        self.device.delay(2)
        self.sdevice(resourceId="com.android.mms:id/embedded_text_editor").set_text(contentm)
        self.device.delay(1)
        self.sdevice(resourceId="com.android.mms:id/send_button_layout").click()
        self.logger.debug("M-device receive msg")
        self.device.open.notification()
        if self.device(text=contentm).wait.exists(timeout=30000):
            self.logger.info("s-device send %s to m-device success" % contentm)
            return True
        else:
            self.logger.info("s-device send %s to m-device failed" % contentm)
            self.save_fail_img()
            return False

    def answer_musicing(self, loop=0):
        """answer s-device message during play music
        """
        contentm = "Message test loop %d" % (loop + 1)
        contents = "Already receive message %d" % (loop + 1)
        self.logger.info("m-device reply %s to s-device and back to music" % contents)
        self.device(text=contentm).click()
        self.device.delay(2)
        self.logger.info("mdvice replay msg %s to sdevice" % contents)
        self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text(contents)
        self.device(description="Send").click()
        self.logger.debug("s-device receive msg")
        if self.sdevice(text=contents).wait.exists(timeout=30000):
            self.logger.info("mdvice replay msg %s to sdevice success" % contents)
            self.logger.info("mdevice back to music")
            for i in range(5):
                self.device.press.back()
                if self.device(packageName="com.alcatel.music5").wait.exists(timeout=2000):
                    self.logger.info("mdevice back to music success")
                    return True
            self.logger.info("mdevice back to music failed")
            self.save_fail_img()
            self.start_app("Music", False)
            return False
        else:
            self.logger.info("mdvice replay msg %s to sdevice failed" % contents)
            self.save_fail_img()
            self.device.press.back()
            return False

    def _verify_msg_sending(self):
        """verify whether the message has received
        """
        self.logger.info("verify send message result")
        if self.device(text='Sending...').exists:
            if self.device(text='Sending...').wait.gone(timeout=180000):
                if self.device(resourceId='com.android.mms:id/date_view').exists:
                    self.logger.debug('message send success!')
                    return True
            self.logger.error('message send fail!!!')
            self.save_fail_img()
            return False
        elif self.device(resourceId='com.android.mms:id/date_view').exists:
            self.logger.debug('message send success!')
            return True
        else:
            self.device.press.back()
            if self.device(resourceId='com.android.mms:id/date_view').exists:
                self.logger.debug('message send success!')
                return True
            self.logger.error('message send fail!!!')
            self.save_fail_img()
            return False

    def select_msg(self, Index=0, strtype=None):
        """select message by specified index.

        Argv:   (int)index -- message order in the list
                (str)strtype -- for stability test.
        Author: Zhx
        """
        if strtype != None:
            self.logger.debug("Select the %s message" %strtype)
            msg_order = {'Audio':0, 'Video':1, 'Photo':2, 'Text':3}
            item = msg_order[strtype]
        else:
            self.logger.debug("Select the %s'st message" %(Index+1))
            item = Index
        self.device(className="android.widget.ListView").child(className="android.widget.RelativeLayout", index=item).click()
        self.device.delay(1)
        if self.device(resourceId="com.android.mms:id/mms_layout_view_parent").wait.exists(timeout=3000):
            return True
        else:
            self.logger.warning("Cannot select the message!")
            return False

    def save_draft(self, msg_type, number):
        """save and send draft message
        arg: msg_type(str) SMS or MMS
        """
        self.logger.debug("Save a %s draft message." % (msg_type))
        self.device(resourceId="com.android.mms:id/floating_action_button").click()
        self.logger.debug("Add a recipient.")

        # you can add a recipient from contacts
        # self.device(resourceId="com.android.mms:id/recipients_picker").click()
        # self.device.delay(2)
        # recipient = self.device(resourceId="android:id/list").child(index=0).child(index=2).get_text()
        # self.device(resourceId="android:id/list").child(index=0).click()
        # self.logger.info("recipient is %s" % recipient)
        # self.device(resourceId="com.android.contacts:id/done").click()

        self.device(resourceId="com.android.mms:id/recipients_editor").set_text(number)
        self.device.delay(2)
        if msg_type == "SMS":
            self.logger.info("save a text sms")
            self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("Test message 0123456789!!!")
        if msg_type == "MMS":
            i = random.randint(2, 3)
            self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("Go Spurs Go 0123456789!!!")
            self.device.delay(2)
            self.device(resourceId="com.android.mms:id/share_button").click()
            if i == 1:
                self.logger.info("save a picture mms")
                self.device(resourceId="com.android.mms:id/take_picture").click()
                if self.device(text="ALLOW").exists:
                    self.device(text="ALLOW").click()
                    self.device.delay()
                self.device(resourceId="com.android.mms:id/shutter_button").click()
                # self.device(resourceId="com.android.mms:id/button_done").click.wait(timeout=2000)
            elif i == 2:
                self.logger.info("save a video mms")
                self.device(resourceId="com.android.mms:id/take_picture").click()
                if self.device(text="ALLOW").exists:
                    self.device(text="ALLOW").click()
                    self.device.delay()
                self.device(resourceId="com.android.mms:id/change_module_button").click()
                self.device.delay(4)  # recorder video 4s
                if self.device(resourceId="com.android.mms:id/shutter_button").exists:
                    self.device(resourceId="com.android.mms:id/shutter_button").click()
                # self.device(resourceId="com.android.mms:id/button_done").click.wait(timeout=2000)
            else:
                self.logger.info("save a audio mms")
                self.device(resourceId="com.android.mms:id/record_audio").click()
                if self.device(text="ALLOW").exists:
                    self.device(text="ALLOW").click()
                    self.device.delay()
                x, y = self.device(resourceId="com.android.mms:id/druation_bar").get_location()
                self.device.swipe(x, y, x + 1, y + 1, 200)
        self.device.delay(2)
        self.back_to_message()
        if self.device(resourceId="com.android.mms:id/draft").exists:
            self.logger.info("Save a  %s draft success!" % msg_type)
            return True
        else:
            self.logger.info("Save a  %s draft failed!" % msg_type)
            self.save_fail_img()
            return False

    def send_draft(self, msg_type):
        self.logger.info("open %s from draft" % msg_type)
        self.device(resourceId="com.android.mms:id/draft").click()
        self.device(description="Send MMS" if msg_type == "MMS" else "Send").click.wait(timeout=2000)
        return self._verify_msg_sending()

    def forward(self, str_option="Forward"):
        """Long touch a msg in tread screen and select the option.

        argv: (str)str_option -- option dispaly in the popup menu.
        author: Zhx
        """
        self.logger.debug("Select message option %s" %(str_option))
        self.device(resourceId="com.android.mms:id/mms_layout_view_parent").long_click()
        self.device.delay(1)
        if self.device(resourceId="com.android.mms:id/custom_select_mode_compose").wait.exists(timeout=2000):
            self.device(resourceId="com.android.mms:id/forward").click()
            self.device.delay(1)
            if self.device(text="New message").wait.exists(timeout=2000):
                return True
            else:
                self.logger.warning("Cannot forward the msg!")
                return False
        else:
            self.logger.warning("Cannot enter msg options!")
            return False
            
            
    def send_msg(self):
        """Touch id(button_with_counter) or "Send" to send message.

        Author: Zhx
        """
        self.logger.debug("Send the message")
        if self.device(descriptionContains="Send").exists:
            self.device(descriptionContains="Send").click()
            self.device.delay(1)
            if self.device(text="New message").wait.exists(timeout=3000):
                self.logger.warning("Cannot press the 'Send' button!")
                return False
            else:
                return True
        else:
            self.logger.warning("Cannot find the 'Send' button!")
            return False
    
            
    def input_recipient(self, sendNum):
        """input recipient number.

        Argv: (str)sendNum -- recipients number
        Author: Zhx
        """
        self.logger.debug("Input recipient %s" %(sendNum))
        self.device(resourceId="com.android.mms:id/recipients_editor").set_text(sendNum)
        self.device.delay(2)
        input_num = self.device(resourceId="com.android.mms:id/recipients_editor").get_text()
        temp = input_num.replace(" ", "")
        if temp == sendNum:
            return self.send_msg()
        else:
            self.logger.warning("Input recipient error!")
            return False
            
    def check_message(self):
        """Check message whether sent successfully.

        Author: Zhx
        """
        self.logger.debug("Check the message whether sent")
        msg_num = self.get_sms_num()
        if msg_num >= 1:
            if not self.select_msg():
                self.logger.warning("Cannot enter the first message!")
                return False
            if self.device(textContains="Sending").exists:
                max_time = 18
                for i in range(max_time):
                    self.logger.debug("Wait for Sending...")
                    if self.device(resourceId="com.android.mms:id/delivered_failed_text").exists:
                        self.logger.warning("Send message failed!")
                        return False
                    elif (self.device(resourceId="com.android.mms:id/date_view").exists and \
                            not self.device(textContains="Sending").exists):
                        self.logger.debug("The message sent")
                        return True
                    else:
                        self.device.delay(10)
                self.logger.warning("Cannot send the message in 5 minutes!")
                return False
            elif self.device(resourceId="com.android.mms:id/delivered_failed_text").exists:
                self.logger.warning("Send message failed!")
                return False
            else:
                self.logger.debug("The message sent")
                return True
        else:
            self.logger.warning("The number of message less than 1 !")
            return False

    def get_sms_num(self):
        """Get the number of messages from the message list
        """
        return self.device(resourceId=self.appconfig.id("id_listitem")).count

    '''def delete_msg(self, name):
        """delete msg from message list
        arg: name(str)  message contact name
        """
        self.device(text=name).click.wait(timeout=2000)
        self.device(description="accessibility overflow label").click.wait(timeout=2000)
        if self.device(text="Discard").exists:
            self.device(text="Discard").click()
        else:
            if self.device(text="Delete").wait.exists(timeout=5000):
                pass
            else:
                self.device(description="accessibility overflow label").click.wait()
            self.device(text="Delete").click.wait(timeout=2000)
            self.device(text="DELETE").click()
        self.logger.debug("delete %s msg completed!!!" % name)'''

    def del_extra_msg(self  , num):
        """ Long press to delete message in the message list
        """
        self.logger.debug("Delete the extra messages")
        max_time = 0
        while self.get_sms_num() > num:
            self.delete_a_msg()
            max_time = max_time + 1
            if max_time > 5:
                self.logger.warning("Too many useless messages!")
                return False
        return True
        
        
    def delete_a_msg(self, Index=0):
        ''' Long press to delete message in the message list

        argv: (int)index -- message order in the list
        author: Zhx
        '''
        self.logger.debug("Delete a message")
        before_num = self.get_sms_num()
        #self.device(className="android.widget.ListView").child(className="android.widget.RelativeLayout", index=Index).long_click()
        self.device.drag(330,220,330,220, steps=10)
        self.device.delay(1)
        if self.device(resourceId="com.android.mms:id/delete").wait.exists(timeout=2000):
            self.device(description="Delete").click()
            self.device.delay(1)
            if self.device(resourceId="android:id/alertTitle").wait.exists(timeout=2000):
                self.device(resourceId="android:id/button1").click()
                self.device.delay(1)
                if self.get_sms_num() == before_num:
                    self.logger.warning("Cannot delete a message!")
                    return False
                else:
                    return True
            else:
                self.logger.warning("No popup confirmation window!")
                return False
        else:
            self.logger.warning("Cannot enter the message menu!")
            return False

        
    def delete_thread(self):
        ''' Delete message thread

        author: Zhx
        '''
        self.logger.debug("Delete message thread")
        if self.device(description="accessibility overflow label").exists:
            self.device(description="accessibility overflow label").click()
            self.device.delay(1)
            self.device(textContains="Delete").click()
            self.device.delay(1)
            if self.device(resourceId="android:id/alertTitle").wait.exists(timeout=2000):
                self.device(resourceId="android:id/button1").click()
                self.device.delay(1)
                if self.device(resourceId="android:id/button1").wait.gone(timeout=2000):
                    return True
                else:
                    self.logger.warning("Cannot delete message thread!")
                    return False
            else:
                self.logger.warning("No popup confirmation window!")
                return False
        else:
            self.logger.warning("Cannot find accessibility overflow label!")
            return False


#if __name__ == '__main__':
    #a = Message("80c08ac6", "Message", "e3a1b0f2")
    # a.enter()
    #a.save_draft("MMS", "10010")
    #a.send_draft("MMS")

