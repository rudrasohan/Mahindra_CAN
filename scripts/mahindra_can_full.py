#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import canlib.canlib as canlib
import time
import thread
from std_msgs.msg import Int16

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

def callback_joy(data):
    global datacc
    global datstr
    global H
    global gear_stat
    global gear_cmd
    global RB_FLAG
    global LB_FLAG
    global RT_DATA
    global LT_DATA
    global status
    global S_flag
    global Ind
    global brake
    '''
    if data.buttons[7]:
	    if S_flag==1:
	         status="stop"
	         S_flag=0
	    else:
	         status="start"
	         S_flag=1
    '''
    #if data.buttons[3]:
    #    datacc+=5
    #elif data.buttons[0]:
    #    datacc-=10
    if data.buttons[2]:
        datstr-=5
    elif data.buttons[1]:
        datstr+=5
    elif (data.axes[4]>0):
        H=1
    elif (data.axes[4]<0):
        H=0
    elif data.axes[1]>0.8:
        gear_cmd="F"
    elif data.axes[1]<-0.8:
        gear_cmd="B"
    elif data.buttons[9]:
        gear_cmd="N"
    elif data.axes[6]==-1:
        Ind="L"
    elif data.axes[6]==1:
        Ind="R"
    elif data.axes[7]==-1:
        Ind="Off"
    elif data.buttons[5]:
        RB_FLAG = 1
    elif data.buttons[4]:
        LB_FLAG = 1
    #elif (-1 <= data.axes[5] <= 1):
        #RT_DATA = 1-data.axes[5]
        #brake =int(50*RT_DATA)   also see line 172
    elif (-1 <= data.axes[3] <= 1):
        LT_DATA = 1-data.axes[3]
    if(datstr<-40):
        datstr=-40
    elif(datstr>40):
        datstr=40
def callback_accel(data):
  global brake
  global datacc
  output = data.data
  if output > 0:
    datacc = output
    brake = 0
  else :
    brake = -(output)
    datacc = 0

def start():
    pub = rospy.Publisher('chatter',Int16,queue_size)
    rospy.init_node('subscribe', anonymous=True)
    rospy.Subscriber("joy",Joy, callback_joy)
    rospy.Subscriber("accel",Int16,callback_accel)
    rospy.spin()

def c_send():
   print 33
   global Ind
   global datacc
   global datstr
   global gear_stat
   global gear_cmd
   global RB_FLAG
   global LB_FLAG
   global RT_DATA
   global LT_DATA
   global brake
   t=0
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
   print 44
   while True:
       msgIdacc = 0x770
       msgacc = [0,0,0,0,0,0,0,1]
       #ch0.write(msgIdacc,msgacc,flg)
       msgIdstr = 0x774
       msgstr = [0,0,0,0,0,0,216,1]
       #ch0.write(msgIdstr,msgstr,flg)
       msgIdbrk = 0X772
       msgbrk = [0,0,0,0,0,0,0,1]
       #ch0.write(msgIdbrk,msgbrk,flg)
       msgIdHW = 0X76D
       msgHW = [0,0,0,0,0,0,0,40]
       #ch0.write(msgIdHW,msgHW,flg)
       msgId = 0X778
       msg = [0,0,0,0,0,0,20,0]
       #ch0.write(msgId,msg,flg)
       msgIdH = 0X776
       msgH = [0,0,0,0,0,0,32,9]
       #ch0.write(msgIdH,msgH,flg)
       val=datstr
      # brake = 0
       if (datstr<0):
           t=2
           val=-datstr
       elif (datstr>0):
           t=1
           val=datstr
       #while(status=="stop"):
        #   pass
       print datacc
       msgacc[7]=2*datacc+1
       msgstr[7]=t+4*val

       if H:
           msgH[7]|=(1<<2)
       else:
           msgH[7]|=(0<<2)
       if Ind=="R":
           msgH[7]&=0b00011111
           msgH[7]|=0b00011001
       elif Ind=="L":
           msgH[7]&=0b10001111
           msgH[7]|=0b10001001
       else:
           msgH[7]&=0b00001111
       if gear_cmd=="N":
           msg=[0,0,0,0,0,0,20,0]
       elif gear_cmd=="B":
           if gear_stat=="F": #apply brake
               msgacc= [0,0,0,0,0,0,0,1]
               datacc=0
               ch0.write(msgIdacc,msgacc,flg)
               msgH[6] = msgH[6]|(1<<6)|(1<<7)
               ch0.write(msgIdH,msgH,flg)
               msgbrk[7] = 201
               ch0.write(msgIdbrk,msgbrk,flg)
               msg=[0,0,0,0,0,0,20,0]  #to go to neutral
               ch0.write(0x778,msg,flg)
           msg=[0,0,0,0,0,0,12,0]
       elif gear_cmd=="F":
           if gear_stat=="B":
               msgacc= [0,0,0,0,0,0,0,1]
               datacc=0
               ch0.write(msgIdacc,msgacc,flg)
               msgH[6] = msgH[6]|(1<<6)|(1<<7)
               ch0.write(msgIdH,msgH,flg)
               msgbrk[7] = 201
               ch0.write(msgIdbrk,msgbrk,flg)
               msg=[0,0,0,0,0,0,20,0]       #to go to neutral
               ch0.write(0x778,msg,flg)
           msg=[0,0,0,0,0,0,36,0]
       if RT_DATA >0:
           msgH[6] = msgH[6]|(1<<6)|(1<<7)
           msgacc= [0,0,0,0,0,0,0,1]
           datacc=0
       if RB_FLAG == 1:                               #for horn
           msgHW[7] = msgHW[7]|(1<<4)
           RB_FLAG = 0
       if LB_FLAG == 1:                                 #for steering reset
           msgstr[6]== msgstr[6]|(1<<5)
           datstr=0
           LB_FLAG = 0
       if LT_DATA > 0:                                    #for wiper
           if LT_DATA < 1:
              msgHW[7]|=(1<<6)
           else:
              msgHW[7]|=(1<<7)
       msgbrk[7] = (2*brake + 1 )
       ch0.write(0x778,msg,flg) #gear
       ch0.write(msgIdH,msgH,flg)
       ch0.write(msgIdacc,msgacc,flg)
       ch0.write(msgIdstr,msgstr,flg)
       ch0.write(msgIdHW,msgHW,flg)
       ch0.write(msgIdbrk,msgbrk,flg)
       time.sleep(10/1000)
def c_recieve():
    global gear_stat
    while True:
        try:
            (msgId, msg, dlc, flg, time) = ch0.read()
            data = ''.join(format(x, '02x') for x in msg)
            if msgId == 0x76C:
                if data[13]=='1':
                  Velocity = int(data[14])*16 + int(data[15])
                  print "velocity : " , velocity
                  pub.publish(velocity)

                else:
                    print "Invalid velocity"
            if msgId == 0x779:
                if msg[6]==8:
                    gear_stat="B"
                elif msg[6]==16:
                    gear_stat="N"
                elif msg[6]==32:
                    gear_stat="F"
            if msgId == 0x773:
                print "Brake:", msg[7]
            print gear_stat
        except:
            pass

if __name__ == '__main__':
    cl = canlib.canlib()
    print("canlib version: %s" % cl.getVersion())


    channel_0 = 0
    ch0 = setUpChannel(channel=0)
    thread.start_new_thread( c_send , ())
    thread.start_new_thread( c_recieve , ())
    start()

    tearDownChannel(ch0)
