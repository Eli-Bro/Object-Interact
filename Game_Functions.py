import math
import random
import cv2


def place_object(dimList, frame, radius, circleColor, prevObjPer=None):
    #Order is width, height since the circle function reflects that order
    objList = []
    objPercents = []
    radius = int(radius)

    if prevObjPer is not None:
        for i, per in enumerate(prevObjPer):
            objList.append(int(per * dimList[i]))
        objPercents = prevObjPer
    else:
        for ele in dimList:
            minCenter = 0 + radius
            maxCenter = ele - radius
            objVal = int(random.uniform(minCenter, maxCenter)) #TODO: After getting rad, use here (for margin)
            objPercent = round(objVal / ele, 2)
            objList.append(objVal)
            objPercents.append(objPercent)

    resultFrame = cv2.circle(frame, (objList[0], objList[1]), radius, circleColor, -1)
    resultFrame = cv2.circle(resultFrame, (objList[0], objList[1]), radius, (0, 0, 0), 3)
    return resultFrame, objPercents


def check_hit(landmarks, objPerList, pose_results, frameList, radius):
    if pose_results.pose_landmarks is None:
        return False

    for ele in landmarks:
        landmarkCenter = [int(pose_results.pose_landmarks.landmark[ele].x * frameList[0]),
                          int(pose_results.pose_landmarks.landmark[ele].y * frameList[1])]
        objCenter = [int(objPerList[0] * frameList[0]), int(objPerList[1] * frameList[1])]
        distance = math.sqrt( ((landmarkCenter[0]-objCenter[0])**2)+((landmarkCenter[1]-objCenter[1])**2) )
        if radius >= distance:
            return True
    return False
