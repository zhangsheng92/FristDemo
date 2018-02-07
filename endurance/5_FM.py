#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.fm import FM


class FmEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        cls.mod = FM(serino, "FM")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('FM Mission Complete')
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
        self.mod.back_to_home()
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def testEndurance(self):
        self.case_switch_fm(int(self.mod.dicttesttimes.get("switch_fm_times".lower())))
        self.case_switch_channel(int(self.mod.dicttesttimes.get("switch_channel_times".lower())))
        self.case_play_fm(int(self.mod.dicttesttimes.get("play_fm_times".lower())))

    def case_switch_fm(self, times):
        self.mod.logger.info("switch FM %d times" % times)
        self.mod.enter()
        self.mod.switch("Stop")
        for loop in range(times):
            try:
                if self.mod.switch("Play") and self.mod.switch("Stop"):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.exit()
        self.mod.back_to_home()
        self.mod.logger.info("switch FM %d times completed" % times)

    def case_switch_channel(self, times):
        self.mod.logger.info("switch channel during play radio %d times" % times)
        for loop in range(times):
            try:
                if self.mod.switch_channel():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("switch channel during play radio %d times" % times)

    def case_play_fm(self, times):
        self.mod.logger.info("Play radio 45 min %d times" % times)
        for loop in range(times):
            try:
                if self.mod.play_fm():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.back_to_home()
        self.mod.logger.info("Play radio 30 min %d times success" % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(FmEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite) 
