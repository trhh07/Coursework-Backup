
import cv2, pandas, serial, time
arduino = serial.Serial('/dev/cu.usbmodem3485187B1B9C2', 9600)  #opens up arduino port for serial communication
time.sleep(2)
txt = 0
with open('ammoCount.txt') as aC: #opens ammo count file to be read later
    ammoC = aC.read()

with open('state.txt') as onOff:  #opens power state file to be read later
    state = onOff.read()

def change(txt,log,rev):     #sub program to change file contents
    file = open(log, 'w')
    if rev == True:      #check to see what the change increment needs to be
        num = -1
    else:
        num = 1
    file.write(str(int(txt)+num))
    file.flush()
    txt = str(int(txt)+num)
    if int(txt) > 0:
        txt = 0
    file.close()
    return(txt)

def auto():                 #sub program to set up automatic firing
    # automatic firing code
    for i in range(4):
        arduino.write(b'fireOn')
        time.sleep(1)
        arduino.write(b'fireOff')

def semi():             #sub program to set up semi automatic firing
    #semi firing code
    arduino.write(b'fireOn')
    time.sleep(1)
    arduino.write(b'fireOff')

def burst():        #sub program to set up burst firing
    #burst firing code
    for i in range(2):
        arduino.write(b'fireOn')
        time.sleep(1)
        arduino.write(b'fireOff')

static_back = None    #intialises empty variable for static comparison frame
motion_list = [None, None]
video = cv2.VideoCapture(0)  #starts live video capture

while True:    #starts a while loop to repeat lines 51-124 indefintely until a file change is detected
    check, frame = video.read()  #sets two variables to contain video frame

    motion = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)      #creates a monochrome image using the video frame

    if static_back is None:
        static_back = gray   #sets the comparison frame equal to the monochrome frame if static_back is equal to None
        continue

    diff_frame = cv2.absdiff(static_back, gray)   #creates a frame that takes the difference of static_back and gray as an image

    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] #creates high contrast image using diff_frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)  #holds the high contrast image back for two iterations so it can be used as a comparison of what the scene used to look like

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)      #uses the threshold frame to create an array of contours (differences of frames)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        motion = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)    #creates green rectangle around the live feed of the colour feed that lines up with contours found to highlight movement
        print(x)
        #start reving motors here
        with open('ammoCount.txt') as aC:      #reads ammo count file to get how many darts left available
            ammoC = aC.read()


        if x > 800 and x < 1050:       #checks to see if movement is within the line of fire of the gun with extra leeway one either side to account for timings for firing
            print('fire')
            arduino.write(b'1')
            with open('fireMode.txt') as fM:
                checkFMde = fM.read()    #uses the contents of fire mode to see what mode the gun is set at and uses if statements to call the right function

            if checkFMde == 'A':
                auto()

            elif checkFMde == 'S':
                semi()

            elif checkFMde == 'B':
                burst()


            txt = change(txt, 'testlog.txt', False)    #updates tally file to indicate when the system detects movement
            ammoC = change(ammoC,'ammoCount.txt', True)    #updates ammo count file with how many bullets where shot
            arduino.write(b'0')
        xs = []
        xs.append(x)

    # stop reving motors here
    motion_list.append(motion)
    motion_list = motion_list[-2:]

    cv2.imshow("Gray Frame", gray)                    #shows all 4 frames
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)            #checks for wheteher or not power state file is equal to ON or OFF with the program terminating if equal to OFF
    with open('state.txt') as onOff:
        state = onOff.read()

    if state == 'OFF':
        if motion == 1:
            static_back = gray

        break
    static_back = gray

video.release()
cv2.destroyAllWindows()    #destroys any window opened by the program

