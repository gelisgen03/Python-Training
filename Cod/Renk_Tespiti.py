import cv2 
import numpy as np
import imutils



def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=-1,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
    window_title = "CSI Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

            while True:

                _,frame = video_capture.read()
                
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                lower_red = np.array([0,100,80])
                upper_red = np.array([10,255,255])
                
                lower_red_iki = np.array([170,100,70])
                upper_red_iki = np.array([180,255,255])

                lower_yellow = np.array([20,100,100])
                upper_yellow = np.array([30,255,255])
                
                lower_green = np.array([40,70,80])
                upper_green = np.array([70,255,255])

                lower_blue = np.array([90,60,0])
                upper_blue = np.array([121,255,255])

                mask_red =  cv2.inRange(hsv, lower_red, upper_red)
                mask_red_iki =  cv2.inRange(hsv, lower_red_iki, upper_red_iki)
                mask1 = mask_red + mask_red_iki
                mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)
                mask3 = cv2.inRange(hsv, lower_green, upper_green)
                mask4 = cv2.inRange(hsv, lower_blue, upper_blue)

                cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts1 = imutils.grab_contours(cnts1)

                cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts2 = imutils.grab_contours(cnts2)

                cnts3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts3 = imutils.grab_contours(cnts3)

                cnts4 = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts4 = imutils.grab_contours(cnts4)

                for c in cnts1:
                    alan1 = cv2.contourArea(c)
                    if alan1 > 5000:
                        print(alan1)
                        cv2.drawContours(frame, [c], -1, (0,255,0), 3)

                        M = cv2.moments(c)

                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        cv2.circle(frame, (cx,cy), 7, (255,255,255), -1)
                        cv2.putText(frame, "Kirmizi", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

                for c in cnts2:
                    alan2 = cv2.contourArea(c)
                    if alan2 > 5000:

                        cv2.drawContours(frame, [c], -1, (0,255,0), 3)

                        M = cv2.moments(c)

                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        cv2.circle(frame, (cx,cy), 7, (255,255,255), -1)
                        cv2.putText(frame, "Sari", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

                for c in cnts3:
                    alan3 = cv2.contourArea(c)
                    if alan3 > 5000:

                        cv2.drawContours(frame, [c], -1, (0,255,0), 3)

                        M = cv2.moments(c)

                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        cv2.circle(frame, (cx,cy), 7, (255,255,255), -1)
                        cv2.putText(frame, "Yesil", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

                for c in cnts4:
                    alan4 = cv2.contourArea(c)
                    if alan4 > 5000:

                        cv2.drawContours(frame, [c], -1, (0,255,0), 3)

                        M = cv2.moments(c)

                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        cv2.circle(frame, (cx,cy), 7, (255,255,255), -1)
                        cv2.putText(frame, "Mavi", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)

                #cv2.imshow("Renk Tespit", frame)
                
                if cv2.waitKey(1) == ord('q'):
                    break


                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break 

                if cv2.waitKey(1) & 0XFF == ord("q"): break
                """
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
                """
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()         






