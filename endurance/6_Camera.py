#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
import traceback

lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not lib_path in sys.path:
    sys.path.append(lib_path)
from common.camera import Camera
from common.settings import Settings


class CameraEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        cls.mod = Camera(serino, "Camera")
        cls.set = Settings(cls.mod.device, "Settings")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Camera Endurance Mission Complete')
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times / cls.mod.test_times * 100
        if Rate < 95:
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def tearDown(self):
        self.mod.logger.info("battery status: %s" % self.mod.adb.shell("dumpsys battery"))

    def test_camera(self):
        #self.case_take_photo(int(self.mod.dicttesttimes.get("photo_times".lower())))
        self.case_take_video(int(self.mod.dicttesttimes.get("video_times".lower())))
        self.case_take_photo_360(int(self.mod.dicttesttimes.get("photo_times_360".lower())))

    def case_take_photo(self, times=1):
        self.mod.logger.info("low storage take photo %d times" % times)
        for loop in range(times):
            try:
                if self.mod.take_photo_to_low():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.warning(e)
                self.mod.save_fail_img()
                self.mod.back_to_home()
        self.mod.back_to_home()
        self.mod.logger.info("low storage take photo %d times completed" % times)
      
    def case_take_photo_360(self, times=1):
        self.mod.logger.info("low storage take photo 360 %d times" % times)
        for loop in range(times):
            try:
                if self.mod.take_photo_360_to_low():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.warning(e)
                self.mod.save_fail_img()
                self.mod.back_to_home()
        self.mod.back_to_home()
        self.mod.logger.info("low storage take photo 360 %d times completed" % times)

    def case_take_video(self, times=1):
        self.mod.logger.info("low storage take video %d times" % times)
        for loop in range(times):
            try:
                if self.mod.take_video_to_low():
                    self.mod.suc_times += 1
                    self.mod.logger.info("Trace Success Loop %s." % (loop + 1))
            except Exception, e:
                self.mod.logger.warning(e)
                self.mod.save_fail_img()
                self.mod.back_to_home()
        self.mod.back_to_home()
        self.mod.logger.info("low storage take video %d times completed" % times)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(CameraEndurance)
    suite = unittest.TestSuite([suite1])
    unittest.TextTestRunner(verbosity=2).run(suite) 

