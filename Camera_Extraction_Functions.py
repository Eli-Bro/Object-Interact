import cv2

'''
Function: display_fps
Takes the difference between previous frame's time and the new frame's time, dividing 1 by that
difference, then displaying it in the top left corner of the camera feed.
'''
def display_fps(frame, newFrameTime, prevFrameTime):
    fps = 1 / (newFrameTime - prevFrameTime)

    # converting the fps into integer then string
    fps = str(int(fps))

    frame = cv2.putText(frame, 'FPS: ' + fps, org=(0, 25), fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        color=(28, 252, 3), thickness=2)
    return frame
