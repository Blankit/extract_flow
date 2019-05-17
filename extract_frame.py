import cv2
#视频切成图片
video_full_path = "IMG_4152.mp4"
cap = cv2.VideoCapture(video_full_path)
print(cap.isOpened())
frame_count = 1
success = True
while (success):
    success, frame = cap.read()#其中ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。frame就是每一帧的图像，是个三维矩阵。'
    # print('Read a new frame: ', success)
    params = []
    # params.append(cv.CV_IMWRITE_PXM_BINARY)
    params.append(1)
    cv2.imwrite("pic_video/video2" + "_%d.jpg" % frame_count, frame)

    frame_count = frame_count + 1

cap.release()
