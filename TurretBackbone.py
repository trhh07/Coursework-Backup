
import cv2, pandas, serial, time
arduino = serial.Serial('/dev/cu.usbmodem3485187B1B9C2', 9600)
time.sleep(2)
txt = 0
with open('ammoCount.txt') as aC:
    ammoC = aC.read()

with open('state.txt') as onOff:
    state = onOff.read()

def change(txt,log,rev):
    file = open(log, 'w')
    if rev == True:
        num = -1
    else:
        num = 1
    file.write(str(txt+str(num)))
    file.flush()
    txt += num
    if txt > 0:
        txt = 0
    file.close()
    return(txt)

def auto():
    # automatic firing code
    for i in range(4):
        arduino.write(b'fireOn')
        time.sleep(1)
        arduino.write(b'fireOff')

def semi():
    #semi firing code
    arduino.write(b'fireOn')
    time.sleep(1)
    arduino.write(b'fireOff')

def burst():
    #burst firing code
    for i in range(2):
        arduino.write(b'fireOn')
        time.sleep(1)
        arduino.write(b'fireOff')

static_back = None
motion_list = [None, None]
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()

    motion = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue

    diff_frame = cv2.absdiff(static_back, gray)

    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        motion = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        print(x)
        #start reving motors here
        with open('ammoCount.txt') as aC:
            ammoC = aC.read()


        if x > 800 and x < 1050:
            print('fire')
            with open('fireMode.txt') as fM:
                checkFMde = fM.read()

            if checkFMde == 'A':
                auto()

            elif checkFMde == 'S':
                semi()

            elif checkFMde == 'B':
                burst()


            txt = change(txt, 'testlog.txt', False)
            ammoC = change(ammoC,'ammoCount.txt', True)

        xs = []
        xs.append(x)

    # stop reving motors here
    motion_list.append(motion)
    motion_list = motion_list[-2:]

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    with open('state.txt') as onOff:
        state = onOff.read()

    if state == 'OFF':
        if motion == 1:
            static_back = gray

        break
    static_back = gray

video.release()
cv2.destroyAllWindows()


