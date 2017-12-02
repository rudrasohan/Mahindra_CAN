#!/usr/bin/env python
import canlib.canlib as canlib
import time
datacc=0
datstr=0
H=0
gear_cmd="F"
gear_stat="F"
RB_FLAG=0
LB_FLAG=0
RT_DATA=0
LT_DATA=0
status="start"
S_flag=1
Ind="Off"
brake = 0
def setUpChannel(channel=0,
                 openFlags=canlib.canOPEN_ACCEPT_VIRTUAL,
                 bitrate=canlib.canBITRATE_500K,
                 bitrateFlags=canlib.canDRIVER_NORMAL):
    cl = canlib.canlib()
    ch = cl.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (ch.getChannelData_Name(),
                                          ch.getChannelData_EAN()))
    ch.setBusOutputControl(bitrateFlags)
    ch.setBusParams(bitrate)
    ch.busOn()
    return ch

def tearDownChannel(ch):
    ch.busOff()
    ch.close()


def c_send():
	while True:
	   flg = canlib.canMSG_STD
	   msgIdacc = 0x770
	   msgacc = [0,0,0,0,0,0,0,1]
	   ch0.write(msgIdacc,msgacc,flg)
	   msgIdstr = 0x774
	   msgstr = [0,0,0,0,0,0,200,0]
	   ch0.write(msgIdstr,msgstr,flg)
	   msgIdbrk = 0X772
	   msgbrk = [0,0,0,0,0,0,0,1]
	   ch0.write(msgIdbrk,msgbrk,flg)
	   msgIdHW = 0X76D
	   msgHW = [0,0,0,0,0,0,0,40]
	   ch0.write(msgIdHW,msgHW,flg)
	   msgId = 0X778
	   msg = [0,0,0,0,0,0,20,0]
	   ch0.write(msgId,msg,flg)
	   msgIdH = 0X776
	   msgH = [0,0,0,0,0,0,32,9]
	   ch0.write(msgIdH,msgH,flg)

if __name__ == '__main__':
    cl = canlib.canlib()
    print("canlib version: %s" % cl.getVersion())


    channel_0 = 0
    ch0 = setUpChannel(channel=0)
    c_send()
    tearDownChannel(ch0)