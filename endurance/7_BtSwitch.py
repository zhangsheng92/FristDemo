#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.settings import Bt


class BtSwitchEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mdevice = "MDEVICE"
        sdevice = "SDEVICE"
        cls.mod = Bt(mdevice, "Btswitch" , sdevice)

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('BT Mission Complete')
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        rate = cls.mod.suc_times / cls.mod.test_times * 100
        if rate < 95:
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(rate) + '%')

    def setUp(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def tearDown(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def testEndurance(self):
        self.case_compare(int(self.mod.dicttesttimes.get("bt_compare_times".lower())))
        self.case_transfer(int(self.mod.dicttesttimes.get("bt_transfer_times".lower())))

    def case_transfer(self, times):
        self.mod.logger.info("m-device transfer file to s-device %d times" % times)
        self.mod.enter_s()
        self.mod.switch_s("ON")
        self.mod.enter()
        self.mod.switch("ON")
        self.mod.compare()
        for loop in range(times):
            try:
                if self.mod.transfer("test_file.mp3"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.warning(e)
                self.mod.save_fail_img()
        self.mod.enter()
        self.mod.cancel_compare()
        self.mod.switch("OFF")
        self.mod.switch_s("OFF")
        self.mod.back_to_home()
        self.mod.back_to_home_s()
        self.mod.logger.info("m-device transfer file to s-device %d times completed" % times)

    def case_compare(self, times=1):
        self.mod.logger.info("m-device compare s-device %d" % times)
        self.mod.enter_s()
        self.mod.switch_s("ON")
        self.mod.enter()
        self.mod.switch("ON")
        for loop in range(times):
            try:
                if self.mod.compare() and self.mod.cancel_compare():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.warning(e)
                self.mod.save_fail_img()
        self.mod.switch_s("OFF")
        self.mod.sdevice.press.back()
        self.mod.sdevice.press.home()
        self.mod.switch("OFF")
        self.mod.back_to_home()
        self.mod.logger.info("m-device compare s-device %d completed" % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(BtSwitchEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite)