# -*- coding: UTF-8 -*-

import sys

def param_to_property(*props, **kwprops):
    if props and kwprops:
        raise SyntaxError("Can not set both props and kwprops at the same time.")

    class Wrapper(object):

        def __init__(self, func):
            self.func = func
            self.kwargs, self.args = {}, []

        def __getattr__(self, attr):
            if kwprops:
                for prop_name, prop_values in kwprops.items():
                    if attr in prop_values and prop_name not in self.kwargs:
                        self.kwargs[prop_name] = attr
                        return self
            elif attr in props:
                self.args.append(attr)
                return self
            raise AttributeError("%s parameter is duplicated or not allowed!" % attr)

        def __call__(self, *args, **kwargs):
            if kwprops:
                kwargs.update(self.kwargs)
                self.kwargs = {}
                return self.func(*args, **kwargs)
            else:
                new_args, self.args = self.args + list(args), []
                return self.func(*new_args, **kwargs)
    return Wrapper


class IDevice(object):  
      
    def click(self,x,y):
        "Perform a click at arbitrary coordinates specified by the user"
        pass    

    def long_click(self, x, y):
        '''long click at arbitrary coordinates.'''
        pass

#     def swipe(self, sx, sy, ex, ey, steps=100):
#         pass

    def drag(self, sx, sy, ex, ey, steps=100):
        '''Swipe from one point to another point.'''
        pass
 
    def screenshot(self,storePath, scale, quality):
        """takeScreenshot(File storePath, float scale, int quality)
        Take a screenshot of current window and store it as PNG The screenshot is adjusted per screen rotation"""
        pass
    
    def wakeup(self):
        """This method simulates pressing the power button if the screen is OFF 
        else it does nothing if the screen is already ON."""
        pass
    def sleep(self):
        """This method simply presses the power button if the screen is ON 
        else it does nothing if the screen is already OFF"""
        pass   
        
    def press(self,key):
        pass
    
#     def slide(self,*arg):
#         pass
#     def get_current_activity(self):
#         pass
#     
#     def get_current_package(self):
#         pass
# 
#     def getDisplayHeight(self):
#         "Gets the height of the display, in pixels."
#         pass
#     
#     def getDisplayWidth(self):
#         "Gets the width of the display, in pixels."
#         pass
#     
#     def is_screen_on(self,device):
#         """check if the screen is on or not"""
#         pass
#     def back_to_home(self):
#         """check if the screen is on or not"""
#         pass 
    
 
class IObject:
    def __init__(self,name,func):
        pass
    def exists(self):
        "Check if UI element exists."
        pass
    " represent a specific UI or activity"
    def waitForExists(self,timeout):
        """Waits a specified length of time for a UI element to become visible."""
        pass

    def waitUntilGone(self,timeout):
        "Waits a specified length of time for a UI element to become undetectable."
        pass

class MetaInterfaceChecker(type):
    def __init__(cls, name, bases, clsdict):
        type.__init__(cls, name, bases, clsdict)

        for i in cls.__implements__:
            required = set(x for x in dir(i) if not x.startswith("_"))
            implemented = set(dir(cls))
            if not required.issubset(implemented):
                raise TypeError("not implemented")

if __name__ == '__main__':
    pass
