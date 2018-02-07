# -*- coding: utf-8 -*-
"""Email library """
import re
import sys
import random
from common import Common,UIParser
from pydoc import classname
from _socket import timeout


class Gmail(Common):

    """Provide common functions involved email."""  
    def __init__(self, device, log_name):
        Common.__init__(self, device, log_name)
        self.appconfig.set_section("Gmail")
        
    def setup(self,accountName,password,type = "pop3"):      
        self.start_app("Email")
        self.device.delay(5)
        if type == "pop3":
            step1 = [
                    #{"id":{"text":self.appconfig("mail_type","Email")}},
                    {"id":{"resourceId":"com.tct.email:id/account_email"},"action":{"type":"set_text","param":[accountName]}},  
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":5000}, 
                    {"id":{"text":"POP3"}},
                    {"id":{"resourceId":"com.tct.email:id/regular_password"},"action":{"type":"set_text","param":[password]}},
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":5000}, 
                    {"id":{"resourceId":"com.tct.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.tct.email:id/account_server"},"action":{"type":"set_text","param":[self.appconfig("mail_server")]}},
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":5000},  
                    {"id":{"resourceId":"com.tct.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.tct.email:id/account_server"},"action":{"type":"set_text","param":[self.appconfig("mail_server")]}},
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":5000},
                    {"id":{"text":"Every 15 minutes"}},
                    {"id":{"text":"Never"}},
                    {"id":{"resourceId":"com.tct.email:id/account_notify"}},
#                     {"id":{"resourceId":"com.tct.email:id/account_sync_email"}},
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":5000}, 
                    {"id":{"resourceId":"com.tct.email:id/account_name"},"action":{"type":"set_text","param":[self.appconfig("mail_name")]}},
                    {"id":{"resourceId":"com.tct.email:id/next"},"delay":8000},
                    {"id":{"resourceId":"com.tct.email:id/dismiss_button"},"delay":5000,"assert":False},
#                     {"id":{"resourceId":"com.tct.email:id/dismiss_button"},"assert":False},
                    {"id":{"description":"Yuan, LI(WMD PIC NB VAL-NB-TCT) about Do our best to do stability and With No Attachment, Hi ; Congratulations on completing your work today.Doing all that extra work while continuing in your position was extremely difficult, and took a lot of effort and dedication on yourpart.I'm sure it on Aug 18, Conversation unread"}},
                    {"id":{"description":"Navigate up"}},
                    {"id":{"description":"Yuan, LI(WMD PIC NB VAL-NB-TCT) about Do our best to test stability and this attachment, Hi ; Congratulations on completing your work today.Doing all that extra work while continuing in your position was extremely difficult, and took a lot of effort and dedication on yourpart.I'm sure it on Aug 18, Conversation unread"}},
                    #{"id":{"className":"android.view.View"}},                   
                    ]

            if UIParser.run(self,step1, self.back_to_mainapp)==False:
                return False
            self.back_to_home() 
#             self.device(scrollable=True).scroll.vert.to(description="Next")
#             step2 = [
#                     {"id":{"description":"Next"},"delay":10000},     
#                     {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},             
#                     {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"set_text","param":[self.appconfig("mail_server")]}},                          
#                     ]
#             if UIParser.run(self,step2, self.back_to_mainapp)==False:
#                 return False
#             self.device(scrollable=True).scroll.vert.to(description="Next")
#             step3 = [
#                     {"id":"description","resourceId":["Next","Next"],"delay":10000},
#                     {"id":{"resourceId":"com.android.email:id/account_name"},"action":{"type":"set_text","param":"CreatedByUIA"}},
#                     {"id":"description","resourceId":["Next","Next"]}               
#                     ]
#             if UIParser.run(self,step3, self.back_to_mainapp)==False:
#                 return False
        elif type == "exchange":
            step1 = [
                    {"id":{"resourceId":"com.android.email:id/account_email"},"action":{"type":"set_text","param":[accountName]}},             
                    {"id":"text","content":["Manual setup","Exchange"]},
                    {"id":{"resourceId":"com.android.email:id/regular_password"},"action":{"type":"set_text","param":[password]}},
                    {"id":{"resourceId":"com.android.email:id/next"},"delay":5000},              
                    {"id":{"resourceId":"com.android.email:id/account_username"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.android.email:id/account_username"},"action":{"type":"set_text","param":[accountName]}}, 
                    {"id":"meta","content":"back"},
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"set_text","param":["mail.tcl.com"]}},                    
                    {"id":"meta","content":"back"},
                    {"id":{"description":"Security type"}},   
                    {"id":{"text":"SSL/TLS (Accept all certificates)"}}, 
                    ]
            if UIParser.run(self,step1, self.back_to_mainapp)==False:
                return False
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step3 = [
                    {"id":{"description":"Next"}},     
                    {"id":{"text":"OK"},"wait":60000},
                    {"id":{"resourceId":"com.android.email:id/account_check_frequency"}},   
                    {"id":{"text":"Manual"}},
                    {"id":{"resourceId":"com.android.email:id/account_sync_window"}},   
                    {"id":{"text":"All"}},                    
                                                      
                    ]
            if UIParser.run(self,step3, self.back_to_mainapp)==False:
                return False            
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step4 = [
                    {"id":{"description":"Next"}},   
                    {"id":{"text":"Activate"},"wait":10000},                   
                    {"id":{"description":"Next"},"wait":30000},                                         
                                                       
                    ]
            if UIParser.run(self,step4, self.back_to_mainapp)==False:
                return False           
            self.device.delay(60)
            self.select_mail(0)
            self.device.delay(5)
            self.select_mail(1)           
            step5 = [
                    {"id":{"resourceId":"com.android.email:id/attachment_icon"},"wait":30000},                                       
                                                       
                    ]
            if UIParser.run(self,step5, self.back_to_mainapp)==False:
                return False               
            self.back_to_mainapp()
        return True
    
    def enter(self):
        """Launch email by StartActivity.
        """
        self.logger.debug("Launch Gmail.")
        if self.device(description=self.appconfig("navigation")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Gmail")
        if self.device(description=self.appconfig("navigation")).wait.exists(timeout=self.timeout):
            return True
        else:
            self.logger.debug('Launch gmail fail')
            return False

    def enter_box(self,box):
        """enter the box you want  
        argv: (str)box --text of the box
        """
        self.logger.debug('enter the box: %s',box)
        if self.device(text=box, index=1).wait.exists(timeout=2000):
            return True
        self.back_to_mainapp()
        if self.device(description=self.appconfig("navigation")).wait.exists(timeout = self.timeout):
            self.device(description=self.appconfig("navigation")).click()
        if self.device(text="Inbox").wait.exists(timeout = self.timeout):
            self.device(scrollable=True).scroll.vert.to(text=box)
            self.device(text=box).click()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot select box: %s" %box)
            self.save_fail_img()
            return False
        if not self.device(text=box, index=1).wait.exists(timeout=5000):
            self.logger.warning("Cannot change to box: %s" %box)
            return False
        return True

    def back(self):
        self.device.press.back()
        return True
    
    def back_to_mainapp(self):
        self.logger.debug("Back to main activity")
        for i in range(5):
            if self.device(description = "Compose").wait.exists(timeout = 2000):
                return True
            self.device.press.back()
        else:
            self.logger.warning("Cannot back to main activity")
            return False

    def loading(self):
        self.device.swipe(500,400,500,1200)
        ui_loading = self.device(resourceId = self.appconfig.id("id_swipe_refresh_widget"))
        if ui_loading.exists:
            self.logger.debug('loading mail')
        
    def forward_gmail(self,address,att_flag):
        """send a email
        argv: (str)address --email address you want to send
              (str)content --email content
        """
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False 
        if self.device(description='Dismiss tip').exists:
            self.device(description='Dismiss tip').click()
            self.device.delay(1)         
            
        self.logger.debug('create an gmail')
        if att_flag:
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).click()
        else:     
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=1).click()
        if self.device(resourceId=self.appconfig.id("id_overflow")).wait.exists(timeout = 5000):
            self.device(resourceId=self.appconfig.id("id_overflow")).click()
        else:
            self.logger.warning('Cannot open an email')
            return False
        if self.device(text='Forward').wait.exists(timeout = 2000):
            self.device(text='Forward').click()
        self.device.delay(2)
        self.device(description='To').set_text(address)
        self.device.delay(2)
        self.device(description='Send').click()
        self.device.delay(2)
        self.logger.debug('email sending...')
        self.device.press.back()
        self.device.delay(2)    
        self.enter_box("Outbox")   
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False 
        if self.device(resourceId = self.appconfig.id("id_empty")).wait.exists(timeout=60000):                        
            return True
        else:
            self.logger.debug('email send fail in 1 min!!!')
            return False
        self.logger.debug('email send fail!!!')
        return False
    
    def del_mail(self,box):
        """delete all email of the box  
        argv: (str)box --text bof the box
        """
        self.logger.debug('delete the mail of %s',box)
        self.enter_box(box)
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            #return False
        if self.device(description = "More options").wait.exists(timeout=2000):
            self.device(description = "More options").click()
        if self.device(text = "Empty Trash").wait.exists(timeout=2000):
            self.device(text = "Empty Trash").click()
            if self.device(text = "Delete").wait.exists(timeout = self.timeout):
                self.device(text = "Delete").click()
                self.device.delay(2)
            if not self.device(resourceId = self.appconfig.id("id_empty")).exists:
                return False  
        else:          
            maxtime=0
#             while not self.device(textContains = self.appconfig("Email","empty_text")).exists:
            while not self.device(resourceId = self.appconfig.id("id_empty")).exists:
                if self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).exists:
                    self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).long_click()
                if self.device(description='Delete').wait.exists(timeout = self.timeout):
                    self.device(description='Delete').click()
                    self.device.delay(2)
                if self.device(description='Discard failed').wait.exists(timeout = self.timeout):
                    self.device(description='Discard failed').click()
                    self.device.delay(2)
                if maxtime>100:
                    return False
                maxtime+=1

        self.logger.debug('mail of the %s has delete complete',box)
        return True

    def select_mail(self,Index):
        self.logger.debug('select the mail of %s',str(Index))
        self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=Index).click()
        self.device.delay(2)
        if self.device(description='Reply').wait.exists(timeout=10000):
            return True
        else:
            self.logger.debug('select mail fail!')
            return False

    def send_gmail(self,address,att_flag,times = 1):
        self.logger.debug("Send with %d attachemnt %d Times" % (att_flag,times))   
        for loop in range (times):
            self.enter_box("Primary")
            try:
                if self.forward_gmail(address,att_flag):
                    self.logger.debug("select mail success")
                    self.suc_times = self.suc_times + 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
                    self.device.press.back() 
                    if self.del_mail('Sent') and self.del_mail('Trash'):
                        self.logger.debug('email send success!!!')
                    else:
                        self.logger.warning("Delete Trash Email Failed")
                        self.save_fail_img()
                else:
                    self.save_fail_img()
                    self.del_mail("Outbox")  
                    self.del_mail('Trash')
            except Exception,e:
                self.save_fail_img()
                #                 common.common.log_traceback(traceback.format_exc())
                self.back_to_mainapp()
                self.enter_box("Primary")
                
    def open_email(self,times):
        self.logger.info('Open Email '+str(times)+' Times')
        for loop in range (times):
            self.enter_box("Primary")
            try:
                if self.select_mail(0):
                    self.logger.debug("select mail success")
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
                    self.device.press.back()
                    self.device.delay(2)
                else:
                    self.save_fail_img()
                    self.enter_box("Primary")
            except Exception,e:
                self.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                self.back_to_mainapp()
                self.enter_box("Primary")
    
    def create_draft(self,address):
        create = [
                    {"id":{"resourceId":self.appconfig.id("id_compose_button")}},   
                    {"id":{"description":"To"},"action":{"type":"set_text","param":[address]}},
                    {"id":{"text":"Compose email"},"action":{"type":"set_text","param":["Stability Test"]}},
                    {"id":{"text":"Subject"},"action":{"type":"set_text","param":["Stability Test"]}},
                    {"id":{"description":self.appconfig("navigation")}},   
                    ]
        if UIParser.run(self,create, self.back_to_mainapp)==False:
            self.logger.debug("Create draft fail!!!") 
            self.save_fail_img()
            return False   
        self.logger.debug("Create draft success!!!")        
        return True  
      
    def send_draft(self):
        self.enter_box("Drafts")
        send = [
                    {"id":{"className":"android.view.View"}},   
                    {"id":{"description":"Edit"}},
                    {"id":{"description":"Send"}},   
                    ]
        if UIParser.run(self,send, self.back_to_mainapp)==False:
            self.logger.debug("Send draft fail!!!") 
            self.save_fail_img()
            return False  
        self.device(description=self.appconfig("navigation")).click()
        if self.device(resourceId=self.appconfig.id("id_empty_view")).wait.exists(timeout=180000):
            self.logger.debug("Send draft success!!!")        
            return True 
        else:
            self.logger.debug("Send draft fail!!!") 
            self.save_fail_img()
            return False

    def case_draft(self,address,times = 1):
        self.logger.debug("Create and send draft %d Times." % times)   
        self.enter() 
        for loop in range (times):
            self.enter_box("Inbox")
            try:
                if self.create_draft(address) and self.send_draft():
                    self.logger.debug("create and send draft success")
                    self.suc_times = self.suc_times + 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
#                     self.device.press.back() 
                    if self.del_mail('Sent') and self.del_mail('Trash'):
                        self.logger.debug('email send success!!!')
                    else:
                        self.logger.warning("Delete Trash Email Failed")
                        self.save_fail_img()
                else:
                    self.save_fail_img()
                    self.del_mail("Outbox")  
                    self.del_mail('Trash')
            except Exception,e:
                self.logger.debug(e)
                self.save_fail_img()
                self.back_to_mainapp()
                self.enter_box("Inbox")
    
    def forward_mail(self,address,att_flag):
        """send a email
        argv: (str)address --email address you want to send
              (str)content --email content
        """
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False 
        self.logger.debug('create an email')
        if att_flag:
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).click()
        else:     
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=1).click()
        if self.device(resourceId=self.appconfig.id("id_overflow")).wait.exists(timeout = 10000):
            self.device(resourceId=self.appconfig.id("id_overflow")).click()
        else:
            self.logger.warning('Cannot open an email')
            return False
        if self.device(text='Forward').wait.exists(timeout = 2000):
            self.device(text='Forward').click()
        if self.device(description='To').wait.exists(timeout = 2000):
            self.device(description='To').set_text(address)
        if self.device(description='Send').wait.exists(timeout = 2000):
            self.device(description='Send').click()
            self.device.delay(2)
        self.logger.debug('email sending...')
        self.back_to_mainapp()
        return self.sending_mail()

    def sending_mail(self):
        self.enter_box("Outbox")
        for loop in range(6):   
            self.loading() 
            if self.device(resourceId = self.appconfig.id("id_empty")).wait.exists(timeout=30000):                        
                return True
        self.logger.debug('email send fail in 3 min!!!')
        return False
    
    def reply_mail(self,i = 0):
        """send a email
        argv: (str)address --email address you want to send
              (str)content --email content
        """
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False   
        self.logger.debug('reply an email')
        if self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=i).wait.exists(timeout=5000):
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=i).click()
        if self.device(description="Reply").wait.exists(timeout = 10000):
            self.device(description="Reply").click()
        else:
            self.logger.warning('Cannot open an email')
            return False
        if self.device(resourceId=self.appconfig.id("id_body")).wait.exists(timeout = 2000):
            self.device(resourceId=self.appconfig.id("id_body")).set_text("0123456789")
        if self.device(description='Send').wait.exists(timeout = 2000):
            self.device(description='Send').click()
            self.device.delay(2)
        self.logger.debug('email sending...')
        self.device.press.back()
        self.device.delay(2)    
        self.enter_box("Outbox")   
        self.loading() 
        if self.device(resourceId = self.appconfig.id("id_empty")).wait.exists(timeout=60000):                        
            return True
        else:
            self.logger.debug('email send fail in 1 min!!!')
            return False
        self.logger.debug('email send fail!!!')
        return False    
    
    def case_send_mail(self,address,att_flag,times = 1):
        self.logger.debug("Send with %d attachemnt %d Times" % (att_flag,times))  
        self.enter() 
        for loop in range (times):
            self.enter_box("Inbox")
            try:
                if self.forward_mail(address,att_flag):
                    self.suc_times = self.suc_times + 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
#                     self.device.press.back() 
                    if self.del_mail('Sent') and self.del_mail('Trash'):
                        self.logger.debug('email send success!!!')
                    else:
                        self.logger.warning("Delete Trash Email Failed")
                        self.save_fail_img()
                else:
                    self.save_fail_img()
                    self.del_mail("Outbox")  
                    self.del_mail('Trash')
            except Exception,e:
                self.save_fail_img()
                self.back_to_mainapp()
                self.enter_box("Inbox")
                
    def case_reply_mail(self, times = 1):
        self.logger.debug("reply a mail %d Times" % times)   
        self.enter() 
        for loop in range (times):
            self.enter_box("Inbox")
            try:
                i=random.randint(0,1)
                if self.reply_mail(i):
                    self.suc_times = self.suc_times + 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
#                     self.device.press.back() 
                    if self.del_mail('Sent') and self.del_mail('Trash'):
                        self.logger.debug('email send success!!!')
                    else:
                        self.logger.warning("Delete Trash Email Failed")
                        self.save_fail_img()
                else:
                    self.save_fail_img()
                    self.del_mail("Outbox")  
                    self.del_mail('Trash')
            except Exception,e:
                self.save_fail_img()
                self.back_to_mainapp()
                self.enter_box("Inbox")
#test--------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    a = Gmail("6670a926","Gmail")
    a.case_send_mail("atttest141@gmail.com",True,1)
    a.case_send_mail("atttest141@gmail.com",False,1)
    a.case_reply_mail(1)
    a.case_draft("atttest141@gmail.com",1)
#     a.forward_mail("atttest141@gmail.com",True)
#     a.loading()
#     a.create_send_draft("yuan-li@tcl.com")
#     a.send_draft()
#     a.enter_box("Drafts")
#     a.del_mail("Trash")
