import cv2
import numpy as np
import copy
import math

cap_region_x_begin=0.5  
cap_region_y_end=0.8  
threshold = 60  
blurValue = 41  
isBgCaptured = 0  
temporalValue = 0
contador_eventos = 0
valor_angulo = 0

def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removerBackground(frame):
    fgmask = algoritmo_extractor_background.apply(frame)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def detectarDedos(frame,figura): 
    hull = cv2.convexHull(frame, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None): 
            cnt = 0
            for i in range(defects.shape[0]):  
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                if angle <= math.pi / 2: 
                    cnt += 1
                    cv2.circle(figura, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, 0




camera = cv2.VideoCapture(0)
camera.set(10,200)
cv2.namedWindow('Cambiar_thresold')
cv2.createTrackbar('trh1', 'Cambiar_thresold', threshold, 100, printThreshold)


while camera.isOpened():
    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'Cambiar_thresold')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    cv2.imshow('original', frame)

    if isBgCaptured == 1: 
        img = removerBackground(frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
        cv2.imshow('mask', img)


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        cv2.imshow('Filtro_Gaussiano', blur)

        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('Imagen_thresold', thresh)
        
        thresh1 = copy.deepcopy(thresh)
        ret,contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length):  # find the biggest contour (according to area)
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)
            drawing = np.zeros(img.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            isFinishCal,cnt = detectarDedos(res,drawing)
            if cnt == temporalValue:
                contador_eventos = contador_eventos + 1

            if contador_eventos ==3:
                valor_angulo = cnt
                print("dedos:" + str(valor_angulo) + "!!")
            elif contador_eventos > 3:
                contador_eventos = 0                                      
            if isFinishCal is True:
                print cnt
                temporalValue = cnt

        if valor_angulo == 0:
            angulo = 0
        elif valor_angulo == 1:
            angulo = 45
        elif valor_angulo == 2:
            angulo = 60

        elif valor_angulo == 3:
            angulo = 90

        elif valor_angulo == 4:
            angulo = 100

        elif valor_angulo == 5:
            angulo = 120

        print("angulo:" + str(angulo))
        cv2.imshow('output', drawing)

    k = cv2.waitKey(10)
    if k == 27:  
        break
    elif k == ord('b'): 
        algoritmo_extractor_background = cv2.createBackgroundSubtractorKNN(detectShadows = True)
        isBgCaptured = 1
        print '!!!Background Captured!!!'
    elif k == ord('r'): 
        algoritmo_extractor_background = None
        isBgCaptured = 0
        print '!!!Reset BackGround!!!'

camera.release
cv2.destroyAllWindows()