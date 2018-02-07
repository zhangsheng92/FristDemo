#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.reboot import Reboot


class RebootEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        cls.mod = Reboot(serino, "Reboot")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Airplane Mission Complete')
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
        self.case_ENDURANCE_REBOOT_001(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_001".lower())))
        #self.case_ENDURANCE_REBOOT_002(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_002".lower())))
        self.case_ENDURANCE_REBOOT_003(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_003".lower())))
        self.case_ENDURANCE_REBOOT_004(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_004".lower())))
        self.case_ENDURANCE_REBOOT_005(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_005".lower())))
        #self.case_ENDURANCE_REBOOT_006(int(self.mod.dicttesttimes.get("ENDURANCE_REBOOT_006".lower())))

    def case_ENDURANCE_REBOOT_001(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)
        
    def case_ENDURANCE_REBOOT_002(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_time_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)
        
    def case_ENDURANCE_REBOOT_003(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_longclick_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)
        
    def case_ENDURANCE_REBOOT_004(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_longclick_withMemoryFull_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)
        
    def case_ENDURANCE_REBOOT_005(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_longclick_withContactsFull_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)
        
    def case_ENDURANCE_REBOOT_006(self, times=1):
        self.mod.logger.info("device reboot %d times" % times)
        for loop in range(times):
            try:
                if self.mod.test_auto_reboot():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %d" % (loop + 1))
            except Exception, e:
                self.mod.logger.info(e)
                self.mod.save_fail_img()
        self.mod.logger.info("restart test %d times completed" % times)


if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(RebootEndurance)
    suite = unittest.TestSuite([suiteCase])
    unittest.TextTestRunner(verbosity=2).run(suite)