import cv2
import winsound

cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    # to find difference between two frames
    diff = cv2.absdiff(frame1, frame2)

    # to remove colors
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # make transition between frames smooth
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # to add sharpness in video
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # to make white parts significant in video
    dilated = cv2.dilate(thresh, None, iterations = 5)

    # find contours in video
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:

        # if countour area is greater then 2000
        if cv2.contourArea(c) < 2000:
            continue

        x, y, w, h = cv2.boundingRect(c)

        # draw rectangle on video
        cv2.rectangle(frame1, (x, y), (x+w,y+h), (255,0,0), 2)

        # alert sound beep for movement
        winsound.Beep(500,200)
        status = cv2.imwrite('Captures/capture.png', frame1)

    # to close press 'q'
    if cv2.waitKey(10) == ord('q'):
        break

    cv2.imshow('Security Camera', frame1)

cam.release()
cv2.destroyAllWindows()