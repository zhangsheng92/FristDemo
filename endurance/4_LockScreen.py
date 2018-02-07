#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.common import *
from common.screen import LockScreen


class LockScreenEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        cls.mod = LockScreen(serino, "LockScreen")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('LockScreen Mission Complete')
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

    def test_lock(self):
        self.case_lock_screen("Swipe", int(self.mod.dicttesttimes.get("SwipeTimes".lower())))
        self.case_lock_screen("Pattern", int(self.mod.dicttesttimes.get("PtnTimes".lower())))
        self.case_lock_screen("PIN", int(self.mod.dicttesttimes.get("PINTimes".lower())))
        self.case_lock_screen("Password", int(self.mod.dicttesttimes.get("PasswordTimes".lower())))
        self.case_switch_wallpaper(int(self.mod.dicttesttimes.get("WallpaperTimes".lower())))

    def case_lock_screen(self, lock_type, times):
        self.mod.logger.info("swipe lock screen %d times" % times)
        password = self.mod.appconfig(lock_type, "LockScreen")
        self.mod.switch_lock_to_lock(lock_type, password)
        for loop in range(times):
            try:
                if self.mod.lock_screen(lock_type, password):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.switch_lock_to_none(lock_type, password)
        self.mod.logger.info("swipe lock screen %d times completed" % times)

    def case_switch_wallpaper(self, times):
        self.mod.logger.info("switch wallpaper %d times" % times)
        for loop in range(times):
            try:
                if self.mod.switch_wallpaper(loop):
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("switch wallpaper %d times completed" % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(LockScreenEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite) 
