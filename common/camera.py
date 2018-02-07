"""Camera library for scripts.
"""

from common import *
from music import Music
from filemanager import FileManager
from automator.adb import Adb


class Camera(Common):

    def __init__(self, device, mod, sdevice=None):
        Common.__init__(self, device, mod, sdevice)
        self.music = Music(self.device, "camera_music")
        self.file = FileManager(self.device, "camera_file")

    def enter(self):
        '''
        Launch camera by StartActivity.
        '''
        if self.device(resourceId=self.appconfig.id("id_shutter", "Camera")).exists:
            return True
        else:
            self.logger.debug('enter camera')
            self.start_activity("com.android.camera" , "com.android.camera.Camera")
            if self.device(resourceId=self.appconfig.id("id_shutter", "Camera")).wait.exists(timeout=2000):
                return True
            else:
                self.logger.debug('enter camera fail!')
                self.save_fail_img()
                return False

    def back_to_camera(self):
        self.logger.debug("Back to camera")
        for i in range(5):
            if self.device(description=self.appconfig("shutter_action", "Camera")).exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to camera")
            self.save_fail_img()
            return False

    def get_photo_number(self):
        return self.get_file_num(self.appconfig("storage_path", "Camera"), ".jpg")

    def get_video_number(self):
        return self.get_file_num(self.appconfig("storage_path", "Camera"), ".3gp")

    def get_number(self, type):
        if type == "photo":
            return self.get_photo_number()
        else:
            return self.get_video_number()

    def switch_picker(self, picker):
        """switch camera picker
        """ 
        self.logger.debug('switch to %s picker' % picker)
        self.device.delay(2)
        if picker.lower() == "back":
            if self.device(resourceId="com.tct.camera:id/hdr_plus_toggle_button").exists:
                self.logger.debug('Already in the back camera')
                return True
            else :
                self.device(resourceId="com.tct.camera:id/camera_toggle_bottom_button").click()
                if self.device(resourceId="com.tct.camera:id/hdr_plus_toggle_button").exists:
                    self.logger.debug('switch to %s picker success' % picker)
                    return True
                else :
                    self.logger.warning("Cannot switch to back camera!")
                    return False
        elif picker == "front":
            if not self.device(resourceId="com.tct.camera:id/hdr_plus_toggle_button").exists:
                self.logger.debug('Already in the front camera')
                return True
            else :
                self.device(resourceId="com.tct.camera:id/camera_toggle_bottom_button").click()
                if not self.device(resourceId="com.tct.camera:id/hdr_plus_toggle_button").exists:
                    self.logger.debug('switch to %s picker success' % picker)
                    return True
                else :
                    self.logger.warning("Cannot switch to front camera!")
                    return False
        else:
            self.logger.debug("Unknown argv: %s, back or front" % picker)
            return False
       
    def take_photo(self):
        """take photo
        """
        self.logger.debug('take photo')
        file_number = self.get_photo_number()
        self.device.delay(1)
        self.device(resourceId="com.tct.camera:id/shutter_button").click()
        self.device.delay(5)
        self.device(resourceId = "com.tct.camera:id/peek_thumb").click()
        if self.device(text="GOT IT").wait.exists(timeout=2000):
            self.device(text="GOT IT").click()
            self.device.delay(1)
        if self.get_photo_number() > file_number:
            self.logger.debug("Take photo success")
            return True
        else:
            self.logger.warning("Take photo failed!")
            self.save_fail_img()
            return False

    def continuous_shooting(self):
        self.logger.debug('take continuous shooting')
        file_number = self.get_photo_number()
        x,y = self.device(resourceId="com.tct.camera:id/shutter_button").get_location()
        self.device.swipe(x, y, x + 1, y + 1, steps=300)
        self.device.delay(5)
        #x, y = self.device(resourceId="com.tct.camera:id/shutter_button").get_location()
        #self.device.swipe(x, y, x + 1, y + 1, steps=300)
        self.start_activity("com.tct.gallery3d" , "com.tct.gallery3d.app.GalleryActivity")
        self.device.delay(3)
        if self.get_photo_number() > file_number:
            self.logger.debug("Take photo success!")
            self.start_activity("com.tct.camera" , "com.android.camera.CameraLauncher")
            return True
        else:
            self.logger.warning("Take photo failed!")
            self.save_fail_img()
            return False

    def preview(self):
        """enter preview mode
        """
        self.logger.debug('enter preview mode')
        if self.device(resourceId="com.tct.camera:id/peek_thumb").wait.exists():
            self.device(resourceId="com.tct.camera:id/peek_thumb").click()
        if self.device(resourceId="com.tct.camera:id/menu_setting_button").wait.gone():
            self.logger.debug('enter preview mode success!')
            return True
        else:
            self.logger.debug('enter preview mode failed!')
            self.save_fail_img()
            return False

    def delete(self, type):
        """delete photo/video in preview mode
        """
        self.logger.debug("Delete %s file" % type)
        if type == "video":
            file_type = ".3gp"
            file_number = self.get_video_number()
        elif type == "photo":
            file_type = ".jpg"
            file_number = self.get_photo_number()
        else:
            self.logger.warning("File extension is invalid!")
            return False
        max_time = 0
        file_number = self.get_file_num(self.appconfig("storage_path", "Camera"), file_type)
        while not self.device(resourceId = "com.tct.gallery3d:id/photopage_delete").exists:
            self.device.click(300, 300)
            self.device.delay(1)
            max_time = max_time + 1
            if max_time > 5:
                self.logger.warning("Cannot show action bar and bottom control!")
                return False
        self.device(resourceId = "com.tct.gallery3d:id/photopage_delete").click()
        if self.device(text = "DELETE").wait.exists(timeout = 2000) :
            self.device(text = "DELETE").click()
            if self.get_file_num(self.appconfig("storage_path", "Camera"), file_type) < file_number:
                self.back_to_camera()
                return True
            else:
                self.logger.warning("Cannot delete %s file!" % type)
                return False
        else :
            self.logger.warning("Cannot find popup window")
            
    def delete_photo(self) :
        # file_number = self.get_file_num(self.appconfig("storage_path", "Camera"), file_type)
        self.start_activity("com.tct.gallery3d" , "com.tct.gallery3d.app.GalleryActivity")
        self.device.delay(1)
        self.device(description = "More options").click()
        self.device.delay(1)
        self.device(text = "Select items").click()
        self.device.delay(1)
        self.device(description = "More options").click()
        self.device.delay(1)
        self.device(text = "Select all").click()
        self.device.delay(1)
        self.device(resourceId = "com.tct.gallery3d:id/action_delete").click()
        if not self.device(text = "DELETE").wait.exists(timeout = 2000) :
            self.logger.debug("Can't find popup window")
            return False
        self.device(text = "DELETE").click()
        self.logger.debug("Delete photo success")
        return True
        
            
        
    

    def record_video(self, duration=30):
        """record video
        argv: (int)recordTime --time of the video
        """
        self.logger.debug('record video')
        file_number = self.get_video_number()
        self.device.delay(2)
        self.device(text = "VIDEO").click()
        self.device(resourceId="com.tct.camera:id/shutter_button").click()
        if not self.device(resourceId="com.tct.camera:id/recording_time").exists:
            self.logger.warning("Cannot record video!")
            return False
        else:
            self.device.delay(duration)
            self.device(resourceId="com.tct.camera:id/shutter_button").click()
            self.device.delay(1)
            self.device(resourceId = "com.tct.camera:id/peek_thumb").click()
            if self.get_video_number() > file_number:
                self.logger.debug("Record video success")
                if self.play_video() :
                    self.logger.debug("play video success")
                    return True
            else:
                self.logger.warning("Record video failed!")
                self.save_fail_img()
                return False

    def play_video(self, duration=30):
        """play video
        """
        self.logger.debug('play video')
        self.adb.shell('input tap 363 651')
        self.device.delay(5)
        if self.is_playing_video() :
            self.logger.debug("play video success")
            self.logger.debug("wait for video play")
            self.device.delay(30)
            return True
        else :
            self.logger.debug("Cannot play video")
            return False


    def takePhoto_duringMusic(self):
        if self.take_photo():
            #self.device.swipe(350, 20, 350, 200, 10)
            self.device.open.notification()
            self.device.delay(2)
            if not self.device(description="Pause").exists:
                self.logger.warning("music isn't playing!!!")
                self.save_fail_img()
                return False
            self.logger.debug("music is playing")
            self.back_to_camera()
            return True

    def take_photo_new(self):
        self.logger.info("take photo")
        if self.enter():
            if self.device(resourceId=self.appconfig.id("id_shutter", "Camera")).wait.exists(timeout=3000):
                self.device(resourceId=self.appconfig.id("id_shutter", "Camera")).click()
                return True

    def take_photo_to_low(self):
        self.logger.info("take photo to low storage")
        self.enter()
        while not (self.device(text="Storage is full").exists or self.device(text="Low memory").exists) :
            if not self.continuous_shooting() :
                break
            self.device.delay(2)
        self.logger.info("phone storage is low")
        self.logger.info("Delete the folder DCIM")
        if self.device(text='CLOSE').exists:
            self.device(text='CLOSE').click()
        if self.device(text='OK').exists:
            self.device(text='OK').click()
        if self.device(text='IGNORE').exists:
            self.device(text='IGNORE').click()
        self.device.delay(3)
        self.start_activity("com.jrdcom.filemanager" , "com.jrdcom.filemanager.activity.FileBrowserActivity")
        return self.file.delete_folder_en("DCIM" , "Phone")
        

    def take_video_to_low(self):
        self.logger.info("take video to low storage")
        self.enter()
        self.logger.info("start to recording video")
        self.device(text ="VIDEO").click()
        self.device.delay(1)
        self.device(resourceId = "com.tct.camera:id/shutter_button").click()
        if self.device(resourceId="com.tct.camera:id/recording_time").wait.exists(timeout = 2000):
            while self.device(resourceId="com.tct.camera:id/recording_time").exists :
                self.device.delay(10)
            self.logger.info("phone storage is low")
            self.logger.info("Delete the folder DCIM")
            if self.device(text='CLOSE').exists:
                self.device(text='CLOSE').click()
            if self.device(text='OK').exists:
                self.device(text='OK').click()
            if self.device(text='IGNORE').exists:
                self.device(text='IGNORE').click()
            #self.device(text='File Manager').click()
            self.device.delay(2)
            #self.device(text="Phone").click()
            self.start_activity("com.jrdcom.filemanager" , "com.jrdcom.filemanager.activity.FileBrowserActivity")
            return self.file.delete_folder_en("DCIM" , "Phone")
        self.logger.info("take video to low storage failed")
        self.save_fail_img()
        return False
        
        
    def take_photo_360_to_low(self) :
        """take photo by 360camera """
        self.enter_360()
        file_number = self.get_photo_number()
        self.device(resourceId = "vStudio.Android.Camera360:id/shutter_btn").click()
        self.device.delay(1)
        self.start_activity("com.tct.gallery3d" , "com.tct.gallery3d.app.GalleryActivity")
        self.device.delay(5)
        #if not self.device(text = "No contents").wait.exists(timeout = 2000) :
        if self.get_photo_number() > file_number:
            self.logger.debug(" 360 Camera Take photo success")
            if self.del_photo() :
                return True
        else:
            self.logger.warning("Take photo failed!")
            self.save_fail_img()
            return False
            
    def del_photo(self) :
        self.device(description = "More options").click()
        self.device.delay(1)
        self.device(text = "Select items").click()
        self.device.delay(1)
        self.device(description = "More options").click()
        self.device.delay(1)
        self.device(text = "Select all").click()
        self.device.delay(1)
        self.device(resourceId = "com.tct.gallery3d:id/action_delete").click()
        if not self.device(text = "DELETE").wait.exists(timeout = 2000) :
            self.logger.debug("Can't find popup window")
            return False
        self.device(text = "DELETE").click()
        self.logger.debug("Delete photo success")
        return True
        
        
    def enter_360(self) :
        self.device.press.home()
        self.start_app("Camera360")
        self.device.delay(1)
        if self.device(resourceId = "vStudio.Android.Camera360:id/shutter_btn").wait.exists(timeout = 2000) :
            self.logger.debug("enter take photo screen success")
            return True
        if self.device(resourceId = "vStudio.Android.Camera360:id/home_user_info_layout").wait.exists(timeout = 2000) :
            self.logger.debug("enter 360 camera success")
            self.device(resourceId = "vStudio.Android.Camera360:id/box1").click()
            if self.device(resourceId = "vStudio.Android.Camera360:id/shutter_btn").wait.exists(timeout = 2000) :
                self.logger.debug("enter take photo screen success")
                return True
            else :
                self.logger.warning("enter take photo screen failed")
                return False
        else :
            self.logger.warning("enter 360 camera failed")
            return False
                


# if __name__ == '__main__':
    # a = Camera("7dab1728", "Camera")
    # a.take_photo_new()
    # a.case_take_photo(2)
    # a.case_record_video(1)
    # a.case_continuous_shooting(1)
    #a.enter()
    #a.record_video()
