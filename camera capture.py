import cv2

key =cv2.waitKey(1)
webcam =cv2.VideoCapture(0)

while True :
    check, frame = webcam.read()
    frame = cv2.flip(frame,1)
    cv2.imshow("Webcam",frame)
    key =cv2.waitKey(1)

    if key == ord("c") :
        cv2.imwrite(filename='001.jpg',img=frame)
        webcam.release()
        print("image capture")
        cv2.destroyAllWindows()
        break
    elif key == ord("s") :
        webcam.release()
        cv2.destroyAllWindows()
        print("camera close")