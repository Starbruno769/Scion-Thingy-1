#import random for dice rolling and the like
import random
#import tkinter for user interfacing
from tkinter import *
from tkinter import ttk
#Basically a copy of the character sheet, but in dictionary form so we can use it
benP = {
    "name": "Benjamin Paige",
    "flight": "Lindwurms",
    "handler": "Nessie",
    "skills": {
        "academics": 4,
        "athletics": 0,
        "closeCombat": 3,
        "culture": 3,
        "empathy": 0,
        "firearms": 0,
        "integrity": 3,
        "leadership": 0,
        "medicine": 0,
        "occult": 3,
        "persuasion": 1,
        "pilot": 0,
        "science": 3,
        "subterfuge": 0,
        "survival": 3,
        "technology": 0
    },
    "attributes":{
        "mental":{
            "intellect": 5,
            "cunning": 3,
            "resolve": 4
        },
        "physical":{
            "might": 3,
            "dexterity": 3,
            "stamina": 1
        },
        "social":{
            "presence": 4,
            "manipulation": 2,
            "composure": 3
        },
    },
    "defense": 4,
    "health":{
        "bruised1": False,
        "bruised2": None,
        "injured1": False,
        "injured2": None,
        "maimed": False
    }
}
#Define some enemy types
mook = {
    "primary": 5,
    "secondary": 4,
    "desperation": 2,
    "health": 1,
    "defense": 1,
    "initiative": 3
}
#make dictionaries for my dictionaries so the combobox later doesn't reveal every variable in existence
cSheets = {
    "benP": benP
}
eTypes = {
    "mook": mook
}
ranges = ["closeCombat","grapple","shortThrown","shortGun","mediumThrown","mediumGun","long"]
#Define the attack function, with "a" being the attacker, "t" the target, "r" the range, and "e" the enhancements for "a"
def attack(a, t, r, e):
    #Initialize the necessary variables
    aPool = 0
    aSuc = 0
    aComp = 0
    #Check the range of the attack and use the respective pool
    if r == "closeCombat":
        aPool = a["skills"]["closeCombat"]+a["attributes"]["physical"]["might"]
    if r == "grapple":
        aPool = a["skills"]["athletics"]+a["attributes"]["physical"]["might"]
    if r == "shortThrown":
        aPool = a["skills"]["athletics"]+a["attributes"]["physical"]["dexterity"]
    if r == "shortGun":
        aPool = a["skills"]["firearms"]+a["attributes"]["physical"]["dexterity"]
    if r == "mediumThrown":
        aPool = a["skills"]["athletics"]+a["attributes"]["mental"]["cunning"]
    if r == "mediumGun":
        aPool = a["skills"]["firearms"]+a["attributes"]["mental"]["cunning"]
    if r == "long":
        aPool = a["skills"]["firearms"]
        if a["attributes"]["mental"]["cunning"]>a["attributes"]["mental"]["intellect"]:
            aPool += a["attributes"]["mental"]["cunning"]
        else:
            aPool += a["attributes"]["mental"]["intellect"]
    #Checks each injury condition for the attacker and adds the respective complication. Yes, I have to check each one individually.
    if a["health"]["bruised1"] == True:
        aComp += 1
    if a["health"]["bruised2"] == True:
        aComp += 1
    if a["health"]["injured1"] == True:
        aComp += 2
    if a["health"]["injured2"] == True:
        aComp += 2
    if a["health"]["maimed"] == True:
        aComp += 4
    #Rolls the dice pool and determines successes
    for x in range(aPool+e):
        roll = random.randint(1,10)
        if roll >= 8:
            aSuc += 1
    #If the successes are higher than "t"s defense, declare a successful attack, otherwise declare a failed attack
    if aSuc > t["defense"]:
        aSuc -= t["defense"]
        print("Attack successful!")
        print("Successes left:")
        print(aSuc)
    else:
        aSuc = 0
        print("Attack failed.")
#Define the defend function, with "a" being the defender, "s" being the attacker's successes, and "f" being whether the defender is "fully defending"
def defend(a, s, f, e):
    #Initialize variables again
    aPool = 0
    aSuc = 0
    aComp = 0
    #If fully defending, do the stuff for that.
    if f == True:
        aPool = a["defense"]*2
    else:
        if a["attributes"]["mental"]["resolve"] >= a["attributes"]["physical"]["stamina"] and a["attributes"]["social"]["composure"]:
            aPool = a["attributes"]["mental"]["resolve"]
        elif a["attributes"]["physical"]["stamina"] >= a["attributes"]["social"]["composure"]:
            aPool = a["attributes"]["physical"]["stamina"]
        else:
            aPool = a["attributes"]["social"]["composure"]
    for x in range(aPool+e):
        roll = random.randint(1,10)
        if roll >= 8:
            aSuc += 1
    if aSuc > s:
        aSuc -= s
        print("Defense successful!")
        print("Successes left:")
        print(aSuc)
    else:
        aSuc = 0
        print("Defense failed.")
#make an interface so the thing is actually usable
root = Tk()
root.title("Scion")
#create a "main frame", hence the name, for the stuff to go in
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#reminder that input functions need their first letter to be uppercase and need a grid position. Also, you can't access values later if you put .grid() in the declaration, you have to do it separately afterward
#these took me way too long to do, tkinter is cursed
#Create the UI elements for the attack section
attackerAL = ttk.Label(mainframe, text="Attacker").grid(column=2, row=1, sticky=W)

attackerA = ttk.Combobox(mainframe, values=list(cSheets.keys()))
attackerA.grid(column=2, row=2, sticky=W)
attackerA.bind("<<ComboboxSelected>>", lambda event: print(attackerA.get()))

targetAL = ttk.Label(mainframe, text="Target").grid(column=3, row=1, sticky=W)

targetA = ttk.Combobox(mainframe, values=list(eTypes.keys()))
targetA.grid(column=3, row=2, sticky=W)
targetA.bind("<<ComboboxSelected>>", lambda event: print(targetA.get()))

rangeAL = ttk.Label(mainframe, text="Range").grid(column=4, row=1, sticky=W)

rangeA = ttk.Combobox(mainframe, values=list(ranges))
rangeA.grid(column=4, row=2, sticky=W)
rangeA.bind("<<ComboboxSelected>>", lambda event: print(rangeA.get()))

enhanceAL = ttk.Label(mainframe, text="Enhancements").grid(column=5, row=1, sticky=W)

enhanceA = ttk.Entry(mainframe)
enhanceA.grid(column=5, row=2, sticky=W)
#Now the ones for the defend section
defenderDL = ttk.Label(mainframe, text="Defender").grid(column=2, row=3, sticky=W)

defenderD = ttk.Combobox(mainframe, values=list(cSheets.keys()))
defenderD.grid(column=2, row=4, sticky=W)

successesDL = ttk.Label(mainframe, text="Enemy Successes").grid(column=3, row=3, sticky=W)

successesD = ttk.Entry(mainframe)
successesD.grid(column=3, row=4, sticky=W)

fullDL = ttk.Label(mainframe, text="Fully Defending").grid(column=4, row=3, sticky=W)

fullD = ttk.Combobox(mainframe, values=[True, False])
fullD.grid(column=4, row=4, sticky=W)

enhanceDL = ttk.Label(mainframe, text="Enhancements").grid(column=5, row=3, sticky=W)

enhanceD = ttk.Entry(mainframe)
enhanceD.grid(column=5, row=4, sticky=W)
#Make the buttons to execute commands
ttk.Button(mainframe, text="Attack", command=lambda: attack(eval(attackerA.get()), eval(targetA.get()), rangeA.get(), int(enhanceA.get()))).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Defend", command=lambda: defend(eval(defenderD.get()), int(successesD.get()), eval(fullD.get()), int(enhanceD.get()))).grid(column=1, row=4, sticky=W)
#ttk.Button(mainframe, text="Add Injury", command=lambda: )
#mainloop makes the ui stay up and constantly run
print("Congrats, nothing has gone wrong yet!") #A silly little message to keep me sane
root.mainloop()
