import tkinter as tk
import time
import os
#import TurretBackbone
settingsF = ['S','B','A']
newTxt = 2

file = open('state.txt', 'w')
file.write('ON')
file.flush()
file.close()


global countA, countOO
countA = 0
countOO = 0
def cycle():
    settingsF = ['S', 'B', 'A']
    value = FireSets["text"]
    countF = settingsF.index(value)
    countF += 1
    if countF == 3:
        countF = 0

    FireSets["text"] = settingsF[countF]
    file = open('fireMode.txt', 'w')
    file.write(settingsF[countF])
    file.flush()
    file.close()

def reset():
    settingsA = ['30', '15', '6']
    global countA
    countA += 1
    if countA == 3:
        countA = 0

    AmmoCount["text"] = settingsA[countA]
    file = open('ammoCount.txt', 'w')
    file.write(settingsA[countA])
    file.flush()
    file.close()

def resetTal():
    file = open('testlog.txt', 'w')
    file.write('0')
    file.flush()
    file.close()

def OnOff():
    state = ['OFF', 'ON']
    global countOO
    countOO += 1
    if countOO == 2:
        countOO = 0
    file = open('state.txt', 'w')
    file.write(state[countOO])
    file.flush()
    file.close()
    if countOO == 0:
        window.destroy()
    #if countOO == 1:
        #exec(open('TurretBackbone.py').read())
        #TurretBackbone.activate()



window = tk.Tk()

window.rowconfigure([0,1,2,3], minsize=50, weight=1)
window.columnconfigure([0,1,2], minsize=50, weight=1)

#=======================================================

Ammo = tk.Label(master=window, text="Ammo Count")
Ammo.grid(row=0, column=1)

AmmoCount = tk.Label(master=window, text="30")
AmmoCount.grid(row=1, column=1)

AmmoReset = tk.Button(master=window, text="Reset", command=reset)
AmmoReset.grid(row=2, column=1, sticky="nsew")

#=======================================================

FireMode = tk.Label(master=window, text="Fire Mode")
FireMode.grid(row=0, column=0)

FireSets = tk.Label(master=window, text="S")
FireSets.grid(row=1, column=0)

cycleF = tk.Button(master=window, text="Cycle", command=cycle)
cycleF.grid(row=2, column=0, sticky="nsew")

#=======================================================

Tally = tk.Label(master=window, text="Tally")
Tally.grid(row=0, column=2)

log = tk.Label(master = window, text='abc')
log.grid(row=1, column=2)

tallyR = tk.Button(master=window, text="Reset", command=resetTal)
tallyR.grid(row=2, column=2, sticky="nsew")

#=======================================================

tOff = tk.Button(master=window, text="OFF", command=OnOff)
tOff.grid(row=3, column=1, sticky='nsew')

#=======================================================

last_mtime = None
tLog = 'testlog.txt'
aCount = 'ammoCount.txt'
def tally_file_change():
    global last_mtime
    mtime = os.path.getmtime(tLog)
    if last_mtime is None or mtime > last_mtime:
        with open(tLog) as f:
            log['text'] = f.read()

        with open(aCount) as f:
            if f.read() == '0':
                AmmoCount['text'] = 'RELOAD'
            else:
                AmmoCount['text'] = f.read()
        last_mtime = mtime
    window.after(1000, tally_file_change)

tally_file_change()
window.mainloop()
