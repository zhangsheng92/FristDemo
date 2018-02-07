#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.settings import NFC
from common.statusbar import StatusBar


class BtEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        if len(sys.argv) > 1:
            serino = sys.argv[1]
        cls.mod = NFC(serino, "NFC")
        cls.bar = StatusBar(cls.mod.device, "statusbar")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('NFC Mission Complete')
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times / cls.mod.test_times * 100
        if Rate < 95:
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def tearDown(self):
        #self.mod.back_to_home()
        #self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def testEndurance(self):
        self.case_set_nfc(int(self.mod.dicttesttimes.get("nfc_in_set".lower())))
        self.case_bar_nfc(int(self.mod.dicttesttimes.get("nfc_in_status".lower())))

    def case_set_nfc(self, times=1):
        self.mod.logger.info("switch NFC %d times in setting" % times)
        self.mod.enter()
        self.mod.switch("OFF")
        for loop in range(times):
            try:
                if self.mod.switch("ON") and self.mod.switch("OFF"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("switch NFC %d times in setting completed" % times)

    def case_bar_nfc(self, times=1):
        self.mod.logger.info("switch nfc %d times in status bar completed" % times)
        self.mod.device.open.quick_settings()
        self.bar.switch_nfc("OFF")
        for loop in range(times):
            try:
                if self.bar.switch_nfc("ON") and self.bar.switch_nfc("OFF"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("switch nfc %d times in status bar completed" % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(BtEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite)