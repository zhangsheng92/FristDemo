#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import random
import os
import sys
import traceback

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.settings import DualSim
from common.telephony import Telephony
from common.message import Message


class DualSimEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        cls.mod = DualSim(serino, "Dualsim")
        cls.tel = Telephony(cls.mod.device, "sim_telephony")
        cls.msg = Message(cls.mod.device, "sim_message")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Airplane Mission Complete')
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        rate = cls.mod.suc_times / cls.mod.test_times * 100
        if rate < 95:
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(rate) + '%')

    def setUp(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery capacity: %s" % self.mod.adb.shell("cat sys/class/power_supply/battery/capacity"))
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("cat sys/class/power_supply/battery/status"))

    def tearDown(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery capacity: %s" % self.mod.adb.shell("cat sys/class/power_supply/battery/capacity"))
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("cat sys/class/power_supply/battery/status"))

    def test_switch(self):
        self.case_switch_sim(1, int(self.mod.dicttesttimes.get("swipe_sim1_set".lower())))
        self.case_switch_sim(2, int(self.mod.dicttesttimes.get("swipe_sim2_set".lower())))
        self.case_switch_data(1, int(self.mod.dicttesttimes.get("swipe_sim1_data_set".lower())))
        self.case_switch_data(2, int(self.mod.dicttesttimes.get("swipe_sim2_data_set".lower())))

    def test_call(self):
        self.case_call("Dialer", int(self.mod.dicttesttimes.get("call_from_dialer_times".lower())))
        self.case_call("Contact", int(self.mod.dicttesttimes.get("call_contact_times".lower())))
        self.case_call("History", int(self.mod.dicttesttimes.get("call_callLog_times".lower())))

    def test_msg(self):
        self.case_forward_msg(int(self.mod.dicttesttimes.get("fwd_msg_times".lower())))

    def case_switch_sim(self, sim_card, times):
        self.mod.logger.info("switch sim card %d %d times" % (sim_card, times))
        self.mod.enter_sim()
        for loop in range(times):
            try:
                if self.mod.switch_sim(sim_card, "OFF") and self.mod.switch_sim(sim_card, "ON"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except:
                self.mod.logger.warning(traceback.format_exc())
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("switch sim card %d %d times completed" % (sim_card, times))

    def case_switch_data(self, sim_card, times):
        self.mod.logger.info("switch sim card %d data %d times" % (sim_card, times))
        self.mod.enter_data()
        for loop in range(times):
            try:
                if self.mod.switch_data(sim_card, "OFF") and self.mod.switch_data(sim_card, "ON"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except:
                self.mod.logger.warning(traceback.format_exc())
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("switch sim card %d data %d times completed" % (sim_card, times))

    def case_call(self, call_type, times):
        """call_type(Dialer、Contact、History)
        """
        self.mod.logger.info("sim1 and sim2 Call from %s %d times." % (call_type, times))
        for loop in range(times):
            try:
                if self.tel.call_10010(call_type, loop, 1) and self.tel.end_call() and self.tel.call_10010(
                        call_type, loop, 2) and self.tel.end_call():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
                else:
                    self.mod.exception_end_call()
            except Exception, e:
                self.mod.logger.error(e)
                self.mod.save_fail_img()
                self.mod.exception_end_call()
            finally:
                self.mod.back_to_home()
        self.mod.logger.info("sim1 and sim2 Call from %s %d times completed" % (call_type, times))

    def case_forward_msg(self, times):
        """case function, forward message case.
        arg: msg_type(str) -- sms or mms.
        """
        self.mod.logger.debug("sim1 and sim2 Send message %s times." % times)
        for loop in range(times):
            try:
                self.msg.enter()
                msg_type = random.choice(["SMS", "MMS"])
                if self.msg.fwd_msg(msg_type, "10010", 1) and self.msg.back_to_message() and self.msg.fwd_msg(
                        msg_type, "10010", 2):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
                self.msg.delete_extra_msg()
            except Exception, e:
                self.mod.logger.error(e)
                self.mod.save_fail_img()
            finally:
                self.mod.back_to_home()
        self.mod.logger.debug("sim1 and sim2 Send message %s times." % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(DualSimEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite) 
