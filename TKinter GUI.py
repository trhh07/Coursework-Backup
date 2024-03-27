import tkinter as tk   #imports the tkinter libary and sets the call phrase as tk
import time
import os
#import TurretBackbone
settingsF = ['S','B','A'] #List set up to hold the values for the different fire modes
newTxt = 2  #Don't know what this is but to scared to delete it

file = open('state.txt', 'w')
file.write('ON')     #changes state.txt to ON when GUI is booted up
file.flush()
file.close()


global countA, countOO  #makes the varaibels to keep track of button state changes for ammo count and on/off global to be used through out the code
countA = 0
countOO = 0
def cycle():#sets up cycle def to be used as a button action that sets the fired mode by cycling through the 3 modes
    settingsF = ['S', 'B', 'A']
    value = FireSets["text"]
    countF = settingsF.index(value)
    countF += 1
    if countF == 3:
        countF = 0

    FireSets["text"] = settingsF[countF] #updates the relevant file with the new value
    file = open('fireMode.txt', 'w')
    file.write(settingsF[countF])
    file.flush()
    file.close()

def reset():#sets up reset def to be used as a button action that both resets the ammo count and cycles through the four choices for it
    settingsA = ['6', '12', '15', '30']
    global countA
    countA += 1
    if countA == 4:
        countA = 0

    AmmoCount["text"] = settingsA[countA]#updates the relevant file with the new value
    file = open('ammoCount.txt', 'w')
    file.write(settingsA[countA])
    file.flush()
    file.close()

def resetTal():   #sets up tally reset def to be used as a button action that just resets tally value to 0 and the corresponfding file
    file = open('testlog.txt', 'w')
    file.write('0')
    file.flush()
    file.close()

def OnOff():  #sets up state change def to be used as a button action that changes the state from on to off
    state = ['OFF', 'ON']
    global countOO
    countOO += 1
    if countOO == 2:
        countOO = 0
    file = open('state.txt', 'w')
    file.write(state[countOO])
    file.flush()
    file.close()
    if countOO == 0: #if state is changed to off the GUI destroys all windows closing itself
        window.destroy()




window = tk.Tk() #creates window

window.rowconfigure([0,1,2,3], minsize=50, weight=1)
window.columnconfigure([0,1,2], minsize=50, weight=1) #configures grid for each cell of gui to be put in

#=======================================================

Ammo = tk.Label(master=window, text="Ammo Count")   #creates title cell for ammo count that reads "Ammo Count"
Ammo.grid(row=0, column=1)

AmmoCount = tk.Label(master=window, text="30")   #creates value cell that reads the current number of ammo left
AmmoCount.grid(row=1, column=1)

AmmoReset = tk.Button(master=window, text="Reset", command=reset) #creates button cell that links to the reset def
AmmoReset.grid(row=2, column=1, sticky="nsew")

#=======================================================

FireMode = tk.Label(master=window, text="Fire Mode") #creates title cell for Fire mode that reads "Fire Mode"
FireMode.grid(row=0, column=0)

FireSets = tk.Label(master=window, text="S")  #creates value cell that reads the current fire mode
FireSets.grid(row=1, column=0)

cycleF = tk.Button(master=window, text="Cycle", command=cycle)   #creates button cell that links to the cycle def
cycleF.grid(row=2, column=0, sticky="nsew")

#=======================================================

Tally = tk.Label(master=window, text="Tally") #creates title cell for tally that reads "Tally"
Tally.grid(row=0, column=2)

log = tk.Label(master = window, text='abc')  #creates value cell that reads the current tally
log.grid(row=1, column=2)

tallyR = tk.Button(master=window, text="Reset", command=resetTal)   #creates button cell that links to the resetTal def
tallyR.grid(row=2, column=2, sticky="nsew")

#=======================================================

tOff = tk.Button(master=window, text="OFF", command=OnOff)   #creates on off button that links to the on off def that read ON but changes to off when pressed
tOff.grid(row=3, column=1, sticky='nsew')

#=======================================================

last_mtime = None
tLog = 'tally.txt'
aCount = 'ammoCount.txt'
def tally_file_change():   #creates subprogram the uses the OS library to make the GUI self updating updating the value of tally and ammo count every 1 second
    global last_mtime
    mtime = os.path.getmtime(aCount)
    if last_mtime is None or mtime > last_mtime:
        with open(tLog) as f:
            firstLine = f.readline()
            log['text'] = firstLine

        with open(aCount) as f:
            firstLine = f.readline()
            if int(firstLine) <= 0:
                AmmoCount['text'] = 'RELOAD'
            else:
                print(f.read())
                AmmoCount['text'] = firstLine
        last_mtime = mtime
    window.after(1000, tally_file_change)

tally_file_change() #calls updater def
window.mainloop()  #loops gui windows until the code is closed or window is destroyed
