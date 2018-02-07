# -*- coding: utf-8 -*-

from common import *


class Schedule(Common):
    """Provide common functions involved Calendar."""

    def enter_calendar(self):
        '''Launch calender by start activity.
        '''
        if self.device(resourceId="com.google.android.calendar:id/overflow").wait.exists():
            return True
        calendar_package = "com.google.android.calendar"
        calendar_activity = "com.android.calendar.AllInOneActivity"
        self.start_activity(calendar_package , calendar_activity)
        while self.device(description="next page").wait.exists(timeout=3000):
            self.device(description="next page").click()
            self.device.delay(1)
        if self.device(text="GOT IT").wait.exists(timeout=2000):
            self.device(text="GOT IT").click()
            self.device.delay(1)
        while self.device(text="ALLOW").wait.exists(timeout=3000):
            self.device(text="ALLOW").click()
            self.device.delay(1)
        if self.device(text="No thanks").wait.exists(timeout=1000):
            self.device(text="No thanks").click()
        return self.device(resourceId="com.google.android.calendar:id/overflow").wait.exists()

    def create_calendar(self, name):
        self.logger.debug('create a new event %s' % name)
        if not self.device(resourceId="com.google.android.calendar:id/floating_action_button").wait.exists(timeout=3000):
            self.logger.warning("Cannot find create new event button")
            return False
        self.device(resourceId="com.google.android.calendar:id/floating_action_button").click()
        if self.device(text="Event").wait.exists(timeout = 3000):
            self.device(text="Event").click()
            self.device.delay(1)
        self.logger.debug('input event %s' % name)
        if self.device(textContains="Events").exists:
            self.device(textContains="Events").click()
            self.device(description="PC Sync").click.wait(timeout=2000)
        self.device(textContains="Enter title").set_text(name)
        self.device.press.back()
        self.device(resourceId="com.google.android.calendar:id/all_day_switch").click()
        self.logger.debug('input event %s location' % name + "_location")
        self.device(text="Add location").click()
        while self.device(text="ALLOW").wait.exists(timeout=3000):
            self.device(text="ALLOW").click()
            self.device.delay(1)
        self.device(text="Add location").set_text(name + "_location")
        self.device.press.back()
        self.device(text="SAVE").click()
        for i in range(2):
            if self.device(description="All day: %s, %s_location" % (name, name)).wait.exists(timeout=2000):
                self.logger.info('create a new event %s success' % name)
                return True
            if self.device(resourceId="com.google.android.calendar:id/week_month_header_arrow").wait.exists(
                    timeout=2000):
                self.device(resourceId="com.google.android.calendar:id/week_month_header_arrow").click()
        self.logger.info('create a new event %s failed' % name)
        self.save_fail_img()
        if self.device(text="Discard").wait.exists(timeout=2000):
            self.device(text="Discard").click()
        return False

    def delete_calendar(self, name):
        self.logger.info("delete the %s events" % name)
        set = [
            {"id": {"description": "All day: %s, %s_location" % (name, name)}},
            {"id": {"description": "More options"}},
            {"id": {"text": "Delete"}},
            {"id": {"text": "OK"}}
        ]
        UIParser.run(self, set)
        self.device.delay(2)
        if not self.device(description="All day: %s, %s_location" % (name, name)).exists:
            self.logger.info("delete the %s events success" % name)
            return True
        else:
            self.logger.info("delete the %s events failed" % name)
            return False

    def enter_alarm(self):
        '''Launch alarm by start activity.
        '''
        if self.device(description="Alarm").exists:
            self.device(description="Alarm").click()
            self.device.delay(1)
            return True
        self.start_app("Clock")
        if self.device(description="Alarm").wait.exists(timeout=2000):
            self.device(description="Alarm").click()
            self.device.delay(1)
            return True
        else:
            return False

    def add_alarm(self):
        """add an alarm without change.
        """
        self.logger.debug("Add an alarm without change.")
        self.device(resourceId="com.google.android.deskclock:id/fab").click()
        self.device(text="OK").click.wait(timeout=2000)
        self.device(resourceId="com.google.android.deskclock:id/arrow").click.wait(timeout=2000)
        for i in range(3):
            if not self.device(resourceId="com.google.android.deskclock:id/onoff", checked=True).exists:
                break
            self.device(resourceId="com.google.android.deskclock:id/onoff", checked=True).click()
            self.device.delay(1)
            self.logger.debug('Add an alarm successfully.')
            return True
        self.logger.debug('alarm add fail!')
        self.save_fail_img()
        return False

    def delete_alarm(self):
        '''Delete alarm.        
        '''
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        self.logger.debug('delete all alarms')
        for i in range(10):
            if self.device(text="No Alarms").exists:
                self.logger.info("delete all alarms success")
                return True
            self.device(resourceId="com.google.android.deskclock:id/arrow").click()
            if self.device(resourceId="com.google.android.deskclock:id/delete").wait.exists():
                self.device(resourceId="com.google.android.deskclock:id/delete").click()
            else:
                self.device(resourceId="com.google.android.deskclock:id/arrow").click()
                self.device(resourceId="com.google.android.deskclock:id/delete").click()
            self.device.delay(2)
        self.logger.info("alarms more than 10")
        self.save_fail_img()
        return False

    def enter_wclock(self):
        '''Launch world clock by start activity.
        '''
        if self.device(description="Clock").exists:
            self.device(description="Clock").click()
            self.device.delay(1)
            return True
        self.start_app("Clock")
        if self.device(description="Clock").wait.exists(timeout=2000):
            self.device(description="Clock").click()
            self.device.delay(1)
            return True
        else:
            return False

    def get_wclock_num(self):
        return self.device(resourceId="com.google.android.deskclock:id/city_name").count

    def add_wclock(self):
        """add world clock without change.
        """
        self.logger.debug("Add two world clocks without change.")
        self.device(resourceId="com.google.android.deskclock:id/fab").click()
        self.device(resourceId="com.google.android.deskclock:id/cities_list").child(index=0).click.wait(timeout=2000)
        self.device(resourceId="com.google.android.deskclock:id/cities_list").child(index=4).click.wait(timeout=2000)
        self.device.delay(1)
        self.device.press.back()
        self.device.delay(1)
        if self.get_wclock_num() >= 2:
            self.logger.debug('Add two world clocks successfully.')
            return True
        else:
            self.logger.debug('world clocks add fail!')
            self.save_fail_img()
            return False

    def delete_wclock(self):
        '''Delete world clocks.
        '''
        self.logger.debug('delete all world clocks')
        self.device(resourceId="com.google.android.deskclock:id/fab").click()
        self.device.delay(2)
        for i in range(5):
            if not self.device(resourceId="com.google.android.deskclock:id/city_onoff", checked=True).exists:
                break
            else:
                self.device(resourceId="com.google.android.deskclock:id/city_onoff", checked=True).click()
                self.device.delay(1)
        self.device.press.back()
        self.device.delay(1)
        if self.get_wclock_num() == 0:
            self.logger.debug('Delete world clocks successfully.')
            return True
        else:
            self.logger.debug('delete world clocks fail!')
            self.save_fail_img()
            return False

    def enter_note(self):
        """Launch Notes by StartActivity.
        """
        self.logger.debug('enter Notes')
        if self.device(packageName="com.tct.note").wait.exists(timeout=5000):
            return True
        self.start_app("Notes")
        if self.device(packageName="com.tct.note").wait.exists(timeout=5000):
            return True

    def get_note_num(self):
        return self.device(resourceId="com.tct.note:id/grid_item").count

    def add_note(self, name):
        """add a note.
        """
        self.logger.debug("Add a note with attachment.")
        self.device(resourceId="com.tct.note:id/newadd_btn2").click()
        self.device.delay(2)
        self.device(resourceId='com.tct.note:id/editview').set_text(name)
        self.device(description="Attachments").click.wait(timeout=1000)
        self.device(text="Gallery").click.wait(timeout=1000)
        self.device(resourceId="com.android.documentsui:id/grid").child(index=0).click.wait(timeout=1000)
        self.device(resourceId="com.tct.note:id/done_menu_item").click.wait(timeout=1000)
        self.device.delay(1)
        if self.get_note_num() >= 1:
            self.logger.debug('Add the note successfully.')
            return True
        else:
            self.logger.debug('Note add fail!')
            self.save_fail_img()
            return False

    def check_note(self, name):
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(textStartsWith=name)
        if self.device(textStartsWith=name).wait.exists(timeout=10000):
            self.device(textStartsWith=name).click()
            if self.device(textStartsWith=name).wait.exists(timeout=10000):
                self.logger.debug('check the note successful')
                self.device.press.back()
                return True
        else:
            self.logger.debug('check fail')
            self.save_fail_img()
            return False

    def delete_note(self, name=None):
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        self.logger.debug('Clean up all the notes')
        for i in range(5):
            if self.device(text="No notes").exists:
                self.logger.info('Clean up all the notes success')
                return True
            self.device(resourceId="com.tct.note:id/card_layout").click()
            self.device(resourceId="com.tct.note:id/view_delete").click()
            self.device(text="OK").click()
            self.device.delay(2)
        self.logger.info("notes more than 5s")
        self.save_fail_img()
        return False

    def add_del_note(self, times=1):
        self.logger.debug('Add and delete note ' + str(times) + ' Times')
        self.enter_note()
        for loop in range(times):
            name = random_name(loop)
            try:
                if self.add_note(name) and self.check_note(name) and self.delete_note():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop " + str(loop + 1))
            except Exception, e:
                self.logger.info(e)
                self.save_fail_img()
                self.delete_note()
        self.back_to_home()
        self.logger.debug('Add and delete note Test complete')


if __name__ == '__main__':
    a = Schedule("80c08ac6", "Schedule")
    # com.google.android.calendar:id/week_month_header_arrow
    # a.enter_calendar()
    a.create_calendar("1111111")

    a.delete_calendar("1111111")


