import time
import pygame
import traceback

import cv2
import mediapipe as mp
from PIL import Image, ImageTk

from GUI_Visual_Resources import *
import Game_Functions as game

global cam
# global recordFlag
global startTime
global frameCap
global objectFlag
global newGame
global objPers
global currRadius
global mirror
global timeSelected
global timeBtns


#Camera feed functions
'''
Function: initiate_cam
The central driver of the overall program, this function handles starting the video feed
and has several calls to processing functions within it. A recording of numerical data
can only begin once the camera has been initialized.
'''
def initiate_cam(placeholder_img, obj_score, start_object_btn, timer_meter, high_score):
    # start_object_btn.config(state=tkinter.NORMAL, bg=startButtonColor)

    global cam
    # Updates record flag to false each time camera is started
    global startTime
    pose, mp_pose, mp_drawing = initialize_pose_estimator()
    global frameCap
    frameCap = False
    global objectFlag
    objectFlag = False
    global newGame
    newGame = True
    global objPers
    objPers = None
    global mirror
    mirror = False

    cam = cv2.VideoCapture(0)
    prevFrameTime = 0
    pygame.mixer.init()

    #TODO: Specific frequency set up
    # Set your desired frequency here (in Hz) (Could be in UI)
    frequency = 5.0  # Run 10 times per second (every 0.1 seconds)
    # Calculate delay from frequency
    delay = 1.0 / frequency
    # Time reference
    start_time = time.time()

    gameStartTime = time.time()*10
    high_score_num = 0

    while cam.isOpened():
        ret, pFrame = cam.read()
        fWidth = pFrame.shape[1]
        fHeight = pFrame.shape[0]
        dimList = [fWidth, fHeight]
        global currRadius

        try:
            #Convert frame to correct color
            pFrame = cv2.cvtColor(pFrame, cv2.COLOR_BGR2RGB)

            # process the frame for pose detection
            pose_results = pose.process(pFrame)
            if pose_results is not None:
                # draw skeleton on the frame
                mp_drawing.draw_landmarks(pFrame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if objectFlag:
                if newGame: # Checks for a new trial
                    objectHit = False
                    score = 0
                    newGame = False
                    pFrame, objPers = game.place_object(dimList, pFrame, currRadius, startCircleColor)
                    prevColor = startCircleColor
                    gameStarted = False
                if objectHit: # Checks if new circle needs to be made
                    pFrame, objPers = game.place_object(dimList, pFrame, currRadius, normalCircleColor)
                    prevColor = normalCircleColor
                    if not gameStarted:
                        for btn in timeBtns:
                            if btn != timeSelected.get():
                                timeBtns[btn].configure(state='disabled')
                        gameStarted = True
                        timer_meter.configure(amounttotal=timeSelected.get(), amountused=timeSelected.get())
                        gameStartTime = time.time()
                        score = 1
                        obj_score.config(text=str(score))
                else: # Keeps the previous circle
                    pFrame, objPers = game.place_object(dimList, pFrame,  currRadius, prevColor, prevObjPer=objPers)
                if game.check_hit(handLandmarks, objPers, pose_results, dimList, currRadius) or \
                        game.check_hit(footLandmarks, objPers, pose_results, dimList, currRadius): # Checks for hit
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(objectHitSound))
                    score += 1
                    obj_score.config(text=str(score))
                    objectHit = True
                else: # No hit detected
                    objectHit = False

                # Check for time
                elapsedGameTime = time.time() - gameStartTime
                timeRemaining = timeSelected.get() - elapsedGameTime
                if gameStarted:
                    timer_meter.configure(amountused=int(timeRemaining))
                else:
                    timer_meter.configure(amountused=timeSelected.get())
                if timeRemaining < 0:
                    if score > high_score_num:
                        high_score.configure(text=str(score))
                        high_score_num = score
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound(highScoreSound))
                    newGame = True
                    gameStartTime = time.time()*10
                    timer_meter.configure(amountused=0)
                    for btn in timeBtns:
                        timeBtns[btn].configure(state='enabled')

            # Handle frame times
            newFrameTime = time.time()

            if not mirror:
                pFrame = cv2.flip(pFrame, 1)

            # Draw all necessary info on frame
            pFrame = game.display_fps(pFrame, newFrameTime, prevFrameTime)
            prevFrameTime = newFrameTime

            # Update the image to tkinter
            pFrame = cv2.resize(pFrame, photoDim)
            img_update = ImageTk.PhotoImage(Image.fromarray(pFrame))
            placeholder_img.configure(image=img_update)
            placeholder_img.image = img_update
            placeholder_img.update()

            if frameCap:
                # Compensate for the time that the codes took to run
                loop_duration = time.time() - start_time
                time.sleep(delay - loop_duration % delay)


        except Exception as e:
            print(e)
            traceback.print_exc()


'''
Function: stop_cam
Stops the active camera feed.
'''
def stop_cam(start_object_btn):
    global cam
    cam.release()
    cv2.destroyAllWindows()
    # start_object_btn.config(state=tkinter.DISABLED, bg=disabledButtonColor)
    print("Stopped!")


'''
Function: initialize_pose_estimator
Creates the tools needed to enact pose estimation via MediaPipe, including drawing utils
and parameters for detection confidence (default is 0.5 for all minimum values).
===
- model complexity: the specific prebuilt model used in the estimation process, in which:
    0 = light (fast, lower accuracy)
    1 = full (medium)
    2 = heavy (slow, higher accuracy)
===
'''
def initialize_pose_estimator():
    # initialize pose estimator
    mp_drawing = mp.solutions.drawing_utils  # Purely for drawing the skeleton on the video
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)  # Parameters for the pose detection
    return pose, mp_pose, mp_drawing


'''
Function: toggle_frame_cap
Controls if the camera is capped at the specific amount of frames during recording,
primarily for keeping the same frequency of data for the machine learning model.
'''
def toggle_frame_cap(toggleMode):
    global frameCap
    if toggleMode.get():
        frameCap = True
    else:
        frameCap = False


def toggle_mirror(toggleMode):
    global mirror
    if toggleMode.get():
        mirror = True
    else:
        mirror = False


'''
Function: select_model
Allows the user to configure the model they need via a file dialog.
'''
def start_object(timeDuration, timeBtnList):
    global objectFlag
    objectFlag = True
    global timeSelected
    timeSelected = timeDuration
    global timeBtns
    timeBtns = timeBtnList

def reset_score(timeBtnList):
    global objectFlag
    objectFlag = False
    global newGame
    newGame = True
    for btn in timeBtns:
        timeBtns[btn].configure(state='enabled')

def resize_scale_circle(radius, preview_img, raw_bg):
    global currRadius
    currRadius = radius
    tmp = cv2.cvtColor(raw_bg, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(raw_bg)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)

    dst = cv2.circle(dst, (int(prevDim[0] / 2), int(prevDim[1] / 2)), int(radius*2), (255, 0, 0, 255), -1)
    dst = cv2.circle(dst, (int(prevDim[0] / 2), int(prevDim[1] / 2)), int(radius*2), (0, 0, 0, 255), 7)

    img_update = ImageTk.PhotoImage(Image.fromarray(dst))
    preview_img.configure(image=img_update)
    preview_img.image = img_update
    preview_img.update()
