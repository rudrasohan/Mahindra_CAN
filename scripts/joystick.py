#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
S_flag=1
H_flag=0
W_flag=0
LI_flag=0
RI_flag=0

def callback(data):
    global H_flag
    global W_flag
    global LI_flag
    global RI_flag
    global S_flag
    H=0
    W=1
    LI=2
    RI=3
    S=7
    if data.buttons[H]:
        if H_flag==1:
            pub.publish("H_OFF")
            H_flag=0
        else:
            pub.publish("H_ON")
            H_flag=1
    if data.buttons[W]:
        if W_flag==1:
            pub.publish("W_OFF")
            W_flag=0
        else:
            pub.publish("W_ON")
            W_flag=1
    if data.buttons[LI]:
        if LI_flag==1:
            pub.publish("LI_OFF")
            LI_flag=0
        else:
            pub.publish("LI_ON")
            LI_flag=1
    if data.buttons[RI]:
        if RI_flag==1:
            pub.publish("RI_OFF")
            RI_flag=0
        else:
            pub.publish("RI_ON")
            RI_flag=1
    if data.buttons[S]:
        if S_flag==1:
            pub.publish("start")
            S_flag=0
        else:
            pub.publish("stop")
            S_flag=1
def start():
	global pub
	pub = rospy.Publisher("chatter", String,queue_size=10)
	rospy.Subscriber("joy",Joy,callback)
	rospy.init_node("JoyPubli")
	rospy.spin()
if __name__ == '__main__':
	start()
