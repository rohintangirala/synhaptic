################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import numpy as np
import Leap, sys, thread, time, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pyautogui
from pyautogui import press, typewrite, hotkey

import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    counter = 0

    def on_frame(self, controller):
        SampleListener.counter += 1
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #if frame.gestures() is not None and SampleListener.counter >= 48:
        #    SampleListener.counter = 0
        for gesture in frame.gestures():
            if gesture is not None:

                gesture = frame.gestures()[0]
                #if gesture.type == SampleListener.previous_gesture:
                if SampleListener.counter > 36:
                    SampleListener.counter = 0
                    hands = frame.hands
                    for hand in hands:

############################################################################
#HandList hands = controller.Hands;
                        lst = []
                        for finger in hand.fingers:
                            if finger.type == 1:
                                lst.append(finger.tip_position)
                            if finger.type == 0:
                                lst.append(finger.tip_position)
                        if lst is not []:
                            origin = Leap.Vector(0, 0, 0)
                            c = lst[1] - lst[0]

                            if origin.distance_to(c) < 20:
                                print 'ok'
                                pyautogui.keyDown('win')
                                press('prntscrn')
                                pyautogui.keyUp('win')
                                users_ref.update({'ok': 1})
                                SampleListener.counter = 0
                                return
##############################################################################
                        if hand.is_left:
                            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                                print 'left key tap'
                                press('enter')
                                users_ref.update({'left key tap': 1})
                            elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
                                print 'left screen tap'
                                users_ref.update({'left screen tap': 1})
                            elif gesture.type is Leap.Gesture.TYPE_SWIPE:
                                swipe = SwipeGesture(gesture)
                                swipeDir = swipe.direction
                                if (swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                                    """
                                    pyautogui.keyDown('ctrl')
                                    press('+')
                                    pyautogui.keyUp('ctrl')
                                    """

                                    pyautogui.keyDown('alt')
                                    pyautogui.keyDown('shift')
                                    press('tab')
                                    pyautogui.keyUp('alt')
                                    pyautogui.keyUp('shift')


                                    print("left-swiped right")
                                    users_ref.update({"left-swiped right": 1})
                                elif (swipeDir.x < 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                                    """
                                    pyautogui.keyDown('ctrl')

                                    press('-')
                                    pyautogui.keyUp('ctrl')
                                    """

                                    pyautogui.keyDown('alt')
                                    press('tab')

                                    pyautogui.keyUp('alt')

                                    print("left-swiped left")
                                    users_ref.update({"left-swiped left": 1})
                                elif (swipeDir.y > 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):

                                    press('volumeup')
                                    press('volumeup')
                                    press('volumeup')
                                    press('volumeup')
                                    press('volumeup')

                                    print("left-swiped up")
                                    users_ref.update({"left-swiped up": 1})
                                elif (swipeDir.y < 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):

                                    press('volumedown')
                                    press('volumedown')
                                    press('volumedown')
                                    press('volumedown')
                                    press('volumedown')

                                    print("left-swiped down")
                                    users_ref.update({"left-swiped down": 1})
                                SampleListener.counter = 0
                            elif gesture.type is Leap.Gesture.TYPE_CIRCLE and gesture.state == 1:
                                """
                                circle = Leap.CircleGesture(gesture)
                                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                                    print("left-clockwise")
                                    pyautogui.scroll(100)
                                    users_ref.update({"left-clockwise": 1})
                                else:
                                    print("left-counterclockwise")
                                    pyautogui.scroll(-100)
                                    users_ref.update({"left-counterclockwise": 1})
                                """
                            SampleListener.counter = 0


                        if hand.is_right:
                            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                                print 'right-key tap'
                                press('space')
                                users_ref.update({'right-key tap': 1})

                            elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
                                print 'right-screen tap'
                                users_ref.update({'right-screen tap': 1})

                            elif gesture.type is Leap.Gesture.TYPE_SWIPE:
                                swipe = SwipeGesture(gesture)
                                swipeDir = swipe.direction
                                if (swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                                    print("right-swiped right")
                                    press('right')
                                    users_ref.update({"right-swiped right": 1})
                                elif (swipeDir.x < 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                                    print("right-swiped left")
                                    press('left')
                                    users_ref.update({'right-swiped left': 1})
                                elif (swipeDir.y > 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                                    print("right-swiped up")
                                    press('esc')
                                    users_ref.update({'right-swiped up': 1})
                                elif (swipeDir.y < 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                                    print("right-swiped down")
                                    pyautogui.keyDown('ctrl')
                                    press('f5')
                                    pyautogui.keyUp('ctrl')
                                    users_ref.update({'right-swiped down': 1})

                            elif gesture.type is Leap.Gesture.TYPE_CIRCLE and gesture.state == 1:
                                """
                                circle = Leap.CircleGesture(gesture)
                                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                                    print("right-clockwise")
                                    pyautogui.keyDown('alt')
                                    pyautogui.keyDown('shift')
                                    press('tab')
                                    pyautogui.keyUp('alt')
                                    pyautogui.keyUp('shift')
                                    users_ref.update({'right-clockwise': 1})
                                else:
                                    print("right-counterclockwise")

                                    pyautogui.keyDown('alt')
                                    press('tab')

                                    pyautogui.keyUp('alt')
                                    users_ref.update({'right-counterclockwise': 1 })
                                """
                            SampleListener.counter = 0

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

cred = credentials.Certificate(r'C:\Users\eusty\Downloads\applink-gestures-firebase-adminsdk-mmoty-33efe8a254.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://applink-gestures.firebaseio.com'
})
ref = db.reference()
users_ref = ref.child('gestures')

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)



    #########################################################

    #default_app = firebase_admin.initialize_app()
    #print(default_app.name)



    ref = db.reference()

    users_ref.set({})
    """
    users_ref.set({
        'left': {
            'swipe': {
                'left_swipe_right': False,
                'left_swipe_left': False,
                'left_swipe_up': False,
                'left_swipe_down': False
            },
            'tap': {
                'date_of_birth': 'December 9, 1906',
                'full_name': 'Grace Hopper'
            }
            'circle': {
                'date_of_birth': 'December 9, 1906',
                'full_name': 'Grace Hopper'
            }
            'touch': {
                'date_of_birth': 'December 9, 1906',
                'full_name': 'Grace Hopper'
            }
        })
        """



    ###############################################################

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
