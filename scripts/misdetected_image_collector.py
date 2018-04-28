#!/usr/bin/env python
# -*- coding: utf-8 -*

import rospy
import cv2
import commands
import os
import sys
import time
import termios

from std_msgs.msg import Bool,String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from e_point_cloud.msg import ImageRange
from std_msgs.msg import String


PKG_PATH = os.path.abspath("../")

class MisdetectedImageCollector:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw',Image,self.ImageCB)
        
        self.bridge = CvBridge()
        self.cv_image = 0
        
    def ImageCB(self,img):
        self.cv_image = self.bridge.imgmsg_to_cv2(img,"bgr8")

    def getKey(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] &= ~termios.ICANON
        new[3] &= ~termios.ECHO
        try:
            termios.tcsetattr(fd,termios.TCSANOW,new)
            input_key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,termios.TCSANOW, old)
        print "You press",input_key
        return input_key
        
    def MisdetectedImageCollector(self):
        input_key = 'none'
        full_image = self.cv_image
        print "Press -t- for take the picture"
        input_key = self.getKey()
        if input_key == 't':
            print self.cv_image
            cv2.imwrite(PKG_PATH+"/image/full_image.png",full_image)
            os.system("sh "+PKG_PATH+'/scripts/start_darknet.sh')
            with open(PKG_PATH+'/darknet/object_point.txt') as f:
                obj_pos = f.readlines()
            f.close()
            print "object_pos is ",len(obj_pos)
            if len(obj_pos) == 1:#end word only
                print 'object does not exist'
                return
            for i in range(len(obj_pos)-1):
                obj_name,l,r,t,b = obj_pos[i].split()
                l,r,t,b = int(l),int(r),int(t),int(b)
                image_name = "obj"+str(i)+".png"
                disp_image = full_image
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.rectangle(disp_image,(l,t),(r,b),(255,0,255),2)
                cv2.putText(disp_image,obj_name,(l,t+8),font,0.5,(0,0,0))
            cv2.imwrite(PKG_PATH+"/image/result.png",disp_image)
            print "write the image"
        else:
            print "invalid key"
            return
        print "Press -s- for save this image"
        input_key = self.getKey()
        if input_key == 's':
            now_time = int(time.time())
            os.system("cp "+PKG_PATH+'/image/full_image.png '
                           +PKG_PATH+'/image/img'+str(now_time)+'.png')
            #cv2.imwrite(PKG_PATH+"/image/img"+str(now_time)+".png",full_image)
            
if __name__ == '__main__':
    rospy.init_node('misdetected_image_collector')
    mimg_collector = MisdetectedImageCollector()
    time.sleep(0.1)#wait for load image
    while not rospy.is_shutdown():
        mimg_collector.MisdetectedImageCollector()
