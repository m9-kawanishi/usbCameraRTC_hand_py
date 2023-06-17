#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file usbCameraRTC_hand_py.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import os
# opencvをインポートする前にこの処理を加えると起動が早くなる
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import sys, cv2
import time, ctypes
import numpy as np
sys.path.append(".")

import define
from define import *

# Import RTM module
import RTC
import OpenRTM_aist


camera_id = 0
shooting = False
cam = 0  # カメラ用インタスタンス
frame = edit_frame = 0 


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
usbcamerartc_hand_py_spec = ["implementation_id", "usbCameraRTC_hand_py", 
         "type_name",         "usbCameraRTC_hand_py", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "kawa", 
         "category",          "Category", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class usbCameraRTC_hand_py
# @brief ModuleDescription
# 
# 
# </rtc-template>
class usbCameraRTC_hand_py(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_id = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        """
        self._idIn = OpenRTM_aist.InPort("id", self._d_id)
        self._d_shootCmd = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._shootCmdIn = OpenRTM_aist.InPort("shootCmd", self._d_shootCmd)
        self._d_focus = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        """
        self._focusIn = OpenRTM_aist.InPort("focus", self._d_focus)
        self._d_image = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._imageOut = OpenRTM_aist.OutPort("image", self._d_image)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("id",self._idIn)
        self.addInPort("shootCmd",self._shootCmdIn)
        self.addInPort("focus",self._focusIn)
		
        # Set OutPort buffers
        self.addOutPort("image",self._imageOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports

        print("usbCameraRTC_hand_py is ready!")
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):

        global cam
        global camera_id

        # カメラIDの到着待ち
        time.sleep(1)

        # カメラIDの入力
        if self._idIn.isNew():
            camera_id = self._idIn.read()
            camera_id = camera_id.data
            print(f"open f{camera_id} now")
        else:
            print("set id=0 now")
        time.sleep(0.5)

        # カメラオープン
        cam = cv2.VideoCapture(camera_id)
        print("cam open")

        # 解像度設定
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, RESOL_PX_W)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOL_PX_W)

        # FPSを設定
        cam.set(cv2.CAP_PROP_FPS, 60)
        # オートフォーカスをオフ
        cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # カメラの自動露光調整をOFFに設定
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
        
        # フォーカス値を設定
        cam.set(cv2.CAP_PROP_FOCUS, FOCUS_VAL)
        # カメラの露光度を調整
        cam.set(cv2.CAP_PROP_EXPOSURE, PROP_VAL)

        # テスト用撮影
        for i in range(10):
            ret, img = cam.read()
        
        # フォルダがなかったら作成
        os.makedirs("./image/", exist_ok=True)

        # 画像保存
        cv2.imwrite("./image/testshot.jpg", img)

        print("== Start process ==\n\n")
    
        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):

        global cam

        cam.release()
    
        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):

        global cam, shooting, camera_id, frame, edit_frame

        # 撮影コマンドの受信
        if self._shootCmdIn.isNew():
            shooting = self._shootCmdIn.read()
            shooting = shooting.data
            print(f"receive shoot")

        if shooting == True:
            # 試写
            for i in range(2):
                img = cam.read()

            # 撮影
            frame  = cam.read(camera_id)

            # 画像記述の変数を宣言する
            Width = ctypes.c_long()
            Height = ctypes.c_long()
            BitsPerPixel = ctypes.c_int()
            colorformat = ctypes.c_int()

            # バッファサイズを計算
            bpp = int(BitsPerPixel.value / 8.0)
            buffer_size = Width.value * Height.value * bpp

            # 出力データポートの設定
            self._d_image.height = RESOL_PX_H
            self._d_image.width = RESOL_PX_W
            print("A")
            self._d_image.bpp = bpp
            print("C")
            self._d_image.pixels = buffer_size
            print("D")

            self._imageOut.write()
            print("E")

            # cv2.imwrite("capture.jpg", frame)

            # 変数リセット
            shooting = False

            print("send image")

        # フォーカス値の更新
        if self._focusIn.isNew():
            focusVal = self._focusIn.read()
            focusVal = focusVal.data
            cam.set(cv2.CAP_PROP_FOCUS, focusVal)
            print(f"set focus {focusVal}")

        # ID設定ポートに届いたデータを捨てる
        # (バッファにたまるのを防ぐ)
        if self._idIn.isNew():
            self._idIn.read()
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def usbCameraRTC_hand_pyInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=usbcamerartc_hand_py_spec)
    manager.registerFactory(profile,
                            usbCameraRTC_hand_py,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    usbCameraRTC_hand_pyInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("usbCameraRTC_hand_py" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

