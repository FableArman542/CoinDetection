import numpy as np
import cv2

def detectCoin (area, debug=False):
    moedas = [    2,        1,   0.5,   0.2,   0.1,  0.05,  0.02, 0.01]
    medias = [20000, 17156.75, 18700, 15721, 11513, 13468, 10546, 7640]
    medias = np.asarray(medias)
    distance = np.abs(area-medias)
    # print("Distancia: ", distance)
    return moedas[np.argmin(distance)]

names = ["P1000697s", "P1000698s", "P1000699s", "P1000703s", "P1000705s", "P1000706s", "P1000709s", "P1000710s", "P1000713s"]

font = cv2.FONT_HERSHEY_SIMPLEX


enable = False

for j in range (len(names)):
    img = cv2.imread(str("imgs/" + names[j] + ".jpg"))

    hsv = img[:,:,2]

    hsv = cv2.add(hsv,np.array([130.0]))

    cv2.imwrite("imgs/Grayscale/" + names[j] + ".jpg", hsv)

    ret2,th2 = cv2.threshold(hsv,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    erode = cv2.morphologyEx(th2, cv2.MORPH_ERODE, kernel)

    cv2.imwrite("imgs/Binarizado/" + names[j] + ".jpg", erode)

    contours, hierarchy = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.imshow('Closing', erode)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cash = 0
    helper = img.copy()
    for i in range(len(contours)):

        approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), False)
        perimeter = cv2.arcLength(contours[i], True)
        area = cv2.contourArea(contours[i])
        circularity = 0
        if area != 0: circularity = (perimeter**2)/(area)
        a = True
        # helper = img.copy()
        if a: #(7 < len(approx) < 18) and area >= 7400:
            print("Perimeter: ", perimeter, "\nArea: ", area, "\nCircularity: ", circularity)
            if area <= 7000: continue
            if circularity >= 13 and circularity <= 14.9:
                if hierarchy[0][i][2] == -1:#detectCoin(area) != 0:
                    # print (hierarchy[0][i][2])
                    center, radius = cv2.minEnclosingCircle(contours[i])
                    c = detectCoin(area)
                    if c > 0.5:
                        txt = str(detectCoin(area)) + " euros"
                    else:
                        txt = str(detectCoin(area)) + " centimos"
                    helper = cv2.circle(img, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), thickness=5)
                    cv2.putText(helper, txt, (int((center[0]) - (radius/2)), int(center[1])),
                                                font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                    # cv2.drawContours(helper, contours[i], -1, (0, 255, 0), thickness=5)
                    print (cash, " DETECT", c)
                    # cv2.imshow(names[j], helper)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    cash = cash + detectCoin(area)
                print("------------------------------")

    txt = "Saldo: " + str(round(cash, 2))
    cv2.putText(helper, txt, (10, 700), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imwrite("imgs/Output/" + names[j] + ".jpg", helper)
    cv2.imshow(names[j], helper)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Cash Amount =", round(cash, 2))
    print("########################################################################")
    if enable: break