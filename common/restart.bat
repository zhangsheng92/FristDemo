adb shell sendevent /dev/input/event1 1 116 1
adb shell sendevent /dev/input/event1 0 0 0
adb shell sleep 3
adb shell sendevent /dev/input/event1 1 116 0
adb shell sendevent /dev/input/event1 0 0 0