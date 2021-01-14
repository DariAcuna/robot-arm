import cv2 as cv
import numpy as np
import serial

capture = cv.VideoCapture(1)
_, frame = capture.read()
rows, cols, _ = frame.shape

x_middle = int(cols / 2)            # object frame lenght to internal middle point
y_middle = int(rows / 2)            # object frame height to internal middle point

xmid = 640 / 2                      # video capture window length to middle point
ymid = 480 / 2                      # video capture window height to middle point

dx = 40
dy = 40

# boolean = 1

# port configuration

ser = serial.Serial()
ser.port = 'COM6'                  # set port
ser.baudrate = 19200                 # to confirm
ser.bytesize = serial.EIGHTBITS     # set bytesize to eight bits
ser.open()                          # open serial port


def receieveNotice():
    # while True:
    #     if ser.read().decode('ascii') == 's':
    #         break
    someChar = ser.read(ser.in_waiting)


def sweep():
    if y_middle < ymid - dy:
        ser.write(b'a')
        print("A")                  # base servo instruction: rotate anticlockwise
        receieveNotice()
    elif y_middle > ymid + dy:
        ser.write(b'b')
        print("B")            # base servo instruction: rotate clockwise
        receieveNotice()
    else:
        return 1                      # base servo instruction: stay still


def stab():
    if x_middle < xmid - dx:
        ser.write(b'c')                # shoulder and elbow servos instruction: move 'forwards'
        print("C")
        receieveNotice()
    elif x_middle > xmid + dx:
        ser.write(b'd')                # shoulder and elbow servos instruction: move 'backwards'
        print("D")
        receieveNotice()
    else:
        return 1


def contractionandinitial():
    ser.write(b't')                    # general instruction: go to contraction amd initial position


while True:
    _, frame = capture.read()
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)     # why?

    # set interval for some colour
    low_colour = np.array([0, 0, 188])
    high_colour = np.array([108, 255, 255])
    colour_mask = cv.inRange(hsv_frame, low_colour, high_colour)

    # create contour
    contours, _ = cv.findContours(colour_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)   # why?
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

    # create contour
    # contoursy, _ = cv.findContours(colour_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)   # why?
    # contoursy = sorted(contoursx, key=lambda y: cv.contourArea(y), reverse=True)

    # frame biggest area of such colour
    for cnt in contours:
        (x, y, w, h) = cv.boundingRect(cnt)

        x_middle = int((x + x + w) / 2)
        y_middle = int((y + y + h) / 2)
        # print(cv.contourArea(cnt))

        break

    # draw line that passes through the middle of the square that frames area
    for cnt in contours:
        if 0 < cv.contourArea(cnt) < 13400:
            cv.line(frame, (x_middle, 0), (x_middle, 480), (0, 255, 0), 2)
            cv.line(frame, (0, y_middle), (640, y_middle), (0, 255, 0), 2)
        break

    cv.imshow('frame', frame)

    # send data to PIC via serial communication
    # if ser.in_waiting > 0:
    #     boolean = 1

    # print(ser.in_waiting)

    for cnt in contours:

        if 0 < cv.contourArea(cnt) < 13400:
            sweep()

            if sweep():
                stab()

                if stab():
                    ser.write(b'j')
                    print("J")
                    receieveNotice()

                else:
                    contractionandinitial()

        break

    key = cv.waitKey(1)

    if key == 27:
        break

capture.release()
cv.destroyAllWindows()      # closes windows after execution

ser.close()                 # closes port
