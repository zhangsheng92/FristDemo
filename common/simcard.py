#!/usr/bin/python
#coding:utf-8
from common import Common, UIParser
import smtplib
import os
from email.mime.text import MIMEText

mail_host = "mail.tcl.com"
mail_user = "atttest01@tcl.com"
mail_pass = "StabilityTest01"
number = "10010"
mark = "101"
class SimCard(Common):
    def get_data(self):
        self.logger.info("get flows data")
        self.start_app("Messaging")
        self.device(description="add new message").click()
        self.device(text="To").set_text(number)
        self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text(mark)
        self.device.press.back()
        self.device(resourceId="com.android.mms:id/send_button_sms").click()
        self.device.delay(60)
        try:
            if self.device(resourceId="com.android.mms:id/history").child(index=1).exists:
                data=self.device(resourceId="com.android.mms:id/history").child(index=1).child(resourceId="com.android.mms:id/text_view").get_text()
                self.device.press.back()
                self.device.press.back()
                return data
            else:
                self.device.press.back()
                self.device.press.back()
                return "get data failed"
        except Exception, e:
                self.logger.error("get flows data fialed")
                self.logger.debug(str(e))

    def send_mail(self, To):
        self.logger.info("send flows data to %s"%To)
        msg = MIMEText(self.get_data(), _subtype="plain", _charset="utf-8")
        msg["Subject"] = "%s device sim卡流量套餐提醒"%(os.environ.get("MDEVICE"))
        msg["From"] = mail_user
        msg["To"] = To
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(mail_user, To, msg.as_string())
            server.close()
            # return True
        except Exception, e:
            self.logger.error(str(e))
            # return False
        self.logger.info("send flows data to %s completed"%To)
class DeviceException():  
    def send_mail_exception(self, To):
        self.logger.info("send flows data to %s"%To)
        msg = MIMEText( 'zxcvbnm', _subtype="plain", _charset="utf-8")
        msg["Subject"] = "device not connected"
        msg["From"] = mail_user
        msg["To"] = To
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user,mail_pass)
            server.sendmail(mail_user, To, msg.as_string())
            server.close()
            return True
        except Exception, e:
            self.logger.error(str(e))
            return False   

if __name__ == '__main__':
    a=SimCard("2cd0de2b", "simcard")
    a.send_mail("jia.huang@tcl.com")