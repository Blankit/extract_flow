import copy
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
frame_num = 0
bound = 20
vidFile = 'demo.mp4'
xFlowFile = 'flow_x'
yFlowFile = 'flow_y'
imgFile = 'img'

cap = cv2.VideoCapture(vidFile)#vidFile换成0，调取摄像头
# cap = cv2.VideoCapture(0)#vidFile换成0，调取摄像头
ret, frame1 = cap.read()
prev_image = copy.copy(frame1)
prev_grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
# print(type(prev_image))
# cv2.imshow('opencv', prev_image)
# cv2.imwrite('beauty4.jpg',prev_image)
# cv2.waitKey()
# k = cv2.waitKey(200) & 0xff
# print(k)
# if k == ord('s'):
#         cv2.imwrite('beauty.png',prev_image)
# else:
#     exit()

'光流计算'
def cast(v, L, H):
    r = 0
    if v > H:
        a = 255
    elif v < L:
        r = 0
    else:
        r = np.round(255 * (v - L) / (H - L))

    return (r)

def convertFlowToImage(flowx, flowy, imgX, imgY, lowerBound, higherBound):
    for i in range(flowx.shape[0]):
        for j in range(flowy.shape[1]):
            x = flowx[i,j]
            y = flowy[i,j]
            imgX[i,j] = cast(x,lowerBound,higherBound)
            imgY[i,j] = cast(y,lowerBound,higherBound)
    return(imgX,imgY)

#
while(1):
    frame_num += 1
    ret, frame2 = cap.read()
    grey = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev_grey,grey, None, 0.702, 5, 10, 2, 7, 1.5, cv2.OPTFLOW_FARNEBACK_GAUSSIAN )
    # mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    # hsv[...,0] = ang*180/np.pi/2
    # hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    # rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    # cv2.imshow('frame2',rgb)
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break
    # elif k == ord('s'):
    #     cv2.imwrite('opticalfb.png',frame2)
    #     cv2.imwrite('opticalhsv.png',rgb)
    flow0, flow1 = cv2.split(flow)
    imgX, imgY = copy.copy(flow0), copy.copy(flow1)
    image = copy.copy(frame2)

    imgX, imgY = convertFlowToImage(flow0, flow1, imgX, imgY, -1. * bound, bound)
    # print('_%04d.jpg'.format(frame_num))
    tmp = '%04d.jpg'%(frame_num)
    cv2.imwrite(os.path.join(xFlowFile,tmp), imgX)
    cv2.imwrite(os.path.join(yFlowFile,tmp), imgY)
    cv2.imwrite(os.path.join(imgFile,tmp), image)
    prev_grey, grey = grey, prev_grey
    prev_image,image = image,prev_image


cap.release()
cv2.destroyAllWindows()