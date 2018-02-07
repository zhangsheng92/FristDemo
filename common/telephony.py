# -*- coding: UTF-8 -*-
"""Telephony library for scripts.
"""
from common import *
from music import Music


class Telephony(Common):

    def __init__(self, device, log_name, sdevice=None):
        Common.__init__(self, device, log_name, sdevice)
        self.music = Music(self.device, "tel_music")

    def enter_dialer(self):
        """Launch dialer by start activity.
        """
        self.logger.debug("Enter Dialer")
        if self.device(resourceId=self.appconfig.id("id_enter", "Dialer")).exists:
            return True
        self.start_app(self.appconfig("name", "Dialer"))
        return self.device(resourceId=self.appconfig.id("id_enter", "Dialer")).wait.exists(timeout=2000)

    def enter_contacts(self):
        """Launch contacts by start activity.
        """
        self.logger.debug("Launch Contacts")
        if self.device(description="Contacts").exists:
            self.device(description="Contacts").click()
            return True
        self.start_app(self.appconfig("name", "Contacts"))
        if self.device(description="Contacts").wait.exists(timeout=2000):
            self.device(description="Contacts").click()
            return True
        self.logger.debug("Launch Contacts Fail")
        return False

    def back_to_contact(self):
        """back to contacts list.
        """
        self.logger.debug("back to all contact")
        for loop in range(5):
            if self.device(description="Contacts").wait.exists(timeout=1000):
                return True
            self.device.press.back()
        return False

    def end_call(self, device="m"):
        """m or s device end the call
        arg: device(str) "m" or "s"
        """
        self.logger.debug("device end call")
        if device == "m":
            if self.device(description="End").wait.exists(timeout=10000):
                self.device(description="End").click()
            if self.device(description="End").wait.gone(timeout=2000):
                self.logger.info("%s-device end call success" % device)
                return True
        elif device == "mu":
            self.device.delay(5)
            self.device.click(720, 2210)
            #if self.device(text="00:05").wait.exists(timeout=10000):
            #    self.device(description="End").click()
            if self.device(description="End").wait.gone(timeout=2000):
                self.logger.info("%s-device end call success" % device)
                return True
        else:
            if self.sdevice(text="00:05").wait.exists(timeout=10000):
                self.sdevice(description="End").click()
            if self.sdevice(description="End").wait.gone(timeout=2000):
                self.logger.info("%s-device end call success" % device)
                return True
        self.logger.info("%s-device end call failed" % device)
        self.save_fail_img()
        return False

    def add_contact(self, path, name, number, enter=False):
        """add contact
        arg: Path("Phone" or "SIM") contact saved path
             name(str) contact saved name
             number(str) contact number
        return: True/False
        """
        self.logger.debug("Add contacts %s to %s" % (name, path))
        if enter:
            self.enter_contacts()
        self.device(resourceId=self.appconfig.id("id_add", "Contacts")).click()
        if path == "SIM" :
            path_text = "SIM-only, unsynced"  
        else : 
            path_text = "Phone-only, unsynced"
        if self.device(text="Add new account").wait.exists(timeout = 2000):
            self.device(text=path_text).click()
        step = [
            {"id": {"resourceId": "com.android.contacts:id/account"}},
            {"id": {"text": path_text}},
            {"id": {"text": "Name"}, "action": {"type": "set_text", "param": [name]}},
            {"id": {"text": "Phone", "className": "android.widget.EditText"},
             "action": {"type": "set_text", "param": [number]}},
            {"id": {"resourceId": "com.android.contacts:id/save_menu_item"}}
        ]
        UIParser.run(self, step)
        self.device.delay(1)
        self.back_to_contact()
        if not self.device(text=name).exists:
            self.device(scrollable=True).scroll.vert.to(text=name)
        if self.device(text=name).exists:
            self.logger.info("add contacts %s success" % name)
            return True
        self.save_fail_img()
        self.logger.info("add contacts %s failed" % name)
        return False

    def delete_contact(self, name, enter=False):
        """delete contact
        arg: name(str) contact name
             enter(boolean) whether need to open contacts
        return: True/False
        """
        self.logger.debug("delete contact %s" % name)
        if enter:
            self.enter_contacts()
        step = [
            {"id": {"text": name}},
            {"id": {"description": "More options"}},
            {"id": {"text": "Delete"}},
            {"id": {"text": "DELETE"}}
        ]
        UIParser.run(self, step)
        self.back_to_contact()
        if not self.device(text=name).exists:
            self.logger.info("delete contact %s success" % name)
            return True
        self.logger.info("delete contact %s failed" % name)
        self.save_fail_img()
        return False

    def back_to_call_app(self, call_type):
        if call_type == "Contact":
            self.back_to_contact()
        else:
            pass

    def start_call_app(self, call_type):
        """arg: call_type ("Dialer"、"Contact"、"History")
        """
        if call_type == "Contact":
            self.enter_contacts()
        else:
            self.enter_dialer()

    def call(self, call_type, index=0, sim_card=1, open_app=False, mutil=False):
        """m-device call s-device from Dialer、Contact、History
        arg: call_type ("Dialer"、"Contact"、"History")
             index(int) call in the contact list which one contact
             sim_card(int) if Dual sim card mode,select 1 or 2
        return: True/False
        """
        self.logger.debug("call from %s" % call_type)
        if call_type == "Dialer":
            if open_app:self.enter_dialer()
            self.logger.debug("Dial Number %s." % self.sdevice_tel)
            if self.device(description="Dial pad").wait.exists():
                self.device(description="Dial pad").click.wait()
            #if not mutil:
                #self.sdevice_tel = "10010"
            for i in self.sdevice_tel:
                self.device(text=i, resourceId="com.android.dialer:id/dialpad_key_number").click()
            # self.device(resourceId="com.android.dialer:id/digits").set_text(self.sdevice_tel)
            # can not find com.android.dialer:id/digits
            self.device(description="dial").click()
            self.device.delay(1)
        elif call_type == "Contact":
            if open_app:self.enter_contacts()
            contact_name = "AutoTest%02d" % (index + 1)
            self.logger.debug("make call from contact %s" % contact_name)
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(textStartsWith=contact_name)
            if self.device(textStartsWith=contact_name).exists:
                self.device(textStartsWith=contact_name).click()
            else:
                self.logger.warning("Cannot find the contact %s" % contact_name)
                self.save_fail_img()
                return False
            self.device(resourceId='com.android.contacts:id/communication_card').click.wait(timeout=2000)
        else:
            if open_app:self.enter_dialer()
            self.device(description=self.appconfig("recent", "Dialer")).click()
            self.device(resourceId="com.android.dialer:id/call_back_action").click.wait(timeout=2000)
        if self.device(resourceId="android:id/select_dialog_listview").wait.exists(timeout=1000):
            self.device(resourceId="android:id/select_dialog_listview").child(index=sim_card-1).click()
        if not mutil:
            self.logger.info("s-device answer call")
            self.sdevice.open.notification()
            if self.sdevice(textStartsWith="Incoming call").wait.exists(timeout=25000):
                self.logger.info("s-device incoming call")
                self.sdevice.delay(1)
                self.sdevice(text="ANSWER").click()
                #self.sdevice.click(500, 800)
            else:
                self.logger.info("s-device answer call failed")
                self.save_fail_img_s()
                return False
        if self.device(description="End").wait.exists(timeout=5000):
            self.logger.debug("Outgoing call success from %s" % call_type)
            return True
        self.logger.debug("Outgoing call failed from %s" % call_type)
        self.save_fail_img()
        self.sdevice.press.back()
        return False

    def call_10010(self, call_type, index=0, sim_card=1, open_app=False):
        """m-device call 10010 from Dialer、Contact、History
        arg: call_type(Dialer、Contact、History)
             index(int) Call in the contact list which one contact
             sim_card(int) if Dual sim card mode,select 1 or 2
        return: True/False
        """
        self.logger.debug("call from %s" % call_type)
        if call_type == "Dialer":
            if open_app:self.enter_dialer()
            #if open_app:self.enter_dialer()
            self.logger.debug("Dial Number 10010.")
            if self.device(description="Dial pad").wait.exists():
                self.device(description="Dial pad").click.wait()
            for i in "10010":
                self.device(text=i, resourceId="com.android.dialer:id/dialpad_key_number").click()
            self.device(description="dial").click()
        elif call_type == "Contact":
            if open_app:self.enter_contacts()
            contact_name = "AutoTest%02d" % (index + 1)
            self.logger.debug("make call from contact %s" % contact_name)
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(textStartsWith=contact_name)
            if self.device(textStartsWith=contact_name).exists:
                self.device(textStartsWith=contact_name).click()
            else:
                self.logger.warning("Cannot find the contact %s" % contact_name)
                self.save_fail_img()
                return False
            self.device(resourceId='com.android.contacts:id/communication_card').click.wait(timeout=2000)
        else:
            if open_app:self.enter_dialer()
            self.device(description=self.appconfig("recent", "Dialer")).click()
            self.device(resourceId="com.android.dialer:id/call_back_action").click.wait(timeout=2000)
        if self.device(resourceId="android:id/select_dialog_listview").wait.exists(timeout=1000):
            self.device(resourceId="android:id/select_dialog_listview").child(index=sim_card-1).click()
        if self.device(description="End").wait.exists(timeout=10000):
            self.logger.debug("Outgoing call success from %s" % call_type)
            return True
        self.logger.debug("Outgoing call failed from %s" % call_type)
        self.save_fail_img()
        self.device.press.back()
        return False

    def s_call(self):
        """s-device call m-device from Dialer"""
        self.logger.info("s_device call m_device")
        data = self.sdevice.server.adb.shell("am start -a android.intent.action.CALL -d tel:%s" % self.mdevice_tel)
        if data.find("Error") > -1:
            self.logger.error("Fail to call m-device.")
            return False
        self.device.open.notification()
        if self.device(text="Incoming call").wait.exists(timeout=20000):
            self.logger.info("m-device incoming call")
            self.device(text="ANSWER").click()
            # if self.device(description="Dialpad").wait.exists(timeout=5000):
            self.logger.debug("m_device Outgoing call success")
            return True
        self.logger.debug("m_device Outgoing call failed")
        self.save_fail_img()
        return False

    def answer_musicing(self):
        """m-device answer s-device call during play music
        return: True/False
        """
        if self.s_call():
            self.logger.debug("answer call during play music success")
            return True
        self.logger.debug("answer call during play music failed")
        return False

    def back_music(self):
        """m-devices close music
        return: True/False
        """
        self.logger.info("back to music and close music")
        if self.device(packageName="com.alcatel.music5").wait.exists():
            self.logger.info("back music success")
            return self.is_playing_music()
        else:
            self.logger.info("back music failed")
            self.save_fail_img()
            return False


#if __name__ == '__main__':
    #a = Telephony("80c08ac6", "Telephony", "e3a1b0f2")
    #a.end_call()
    # a.call("Contact", open_app=True)
    # a.end_call()
    # a.add_contact("SIM","a11","10010",True)
    # a.delete_contact("a11")
    # a.add_del_contact("SIM")
    # a.Call("Dialer")
    # a.Call("Contacts")
    # a.Call("History")
    # a.add_message_contact()