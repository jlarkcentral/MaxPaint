'''
Utils
'''
import sys
import pygame
import math
import random
import shelve
sys.path.append('../lib/pyganim/')
import pyganim


plusOneAnimBlue = pyganim.loadAnim('../img/anims/plusOne/blue/',0.05)
plusOneAnimYellow = pyganim.loadAnim('../img/anims/plusOne/yellow/',0.05)
plusOneAnimRed = pyganim.loadAnim('../img/anims/plusOne/red/',0.05)

questions = ["What's your name ?",
            "Are you alone ?",
            "Do you need anything ?",
            "Do you know where you are ?",
            "How do you feel ?",
            "Would you like to talk to me now?",
            "Is this the end ?"]
answers = [["This is none of your business.", "Who are YOU ?", "I don't remember..."],
            ["No, there was someone at the end of the previous level !", "Yes, fortunately nobody is with me.", "I should go back to check..."],
            ["I need to slow time...", "I need more protection.", "Give me a weapon, I need to defend myself !"],
            ["This is Heaven...", "Clearly I'm in Hell.", "Of course, I'm in the middle of a game !"],
            ["Not too well, I feel like I've died a thousand times.", "To be honest this isn't much fun...", "I'm on fire, nothing can stop me !"],
            ["I'd rather not.", "I never wanted to talk to you in the first place !", "I wish, but this is not implemented in the game..."],
            ["It'd better be, I'm wasting my time here.", "Isn't there another level ?", "Gnnnnraaaaaahh !!"]
            ]

def save(objectList):
    shelfFile = shelve.open('savegame')
    for name,obj in objectList:
        shelfFile[name] = obj
    shelfFile.close()

def exist(name):
    shelfFile = shelve.open('savegame')
    return (name in shelfFile)

def load(name):
    shelfFile = shelve.open('savegame')
    obj = shelfFile[name]
    shelfFile.close()
    return obj



def getFont(fontName, fontSize):
    return pygame.font.Font('../fonts/'+fontName+'.ttf', fontSize)

def getQuestion(ind):
    return questions[ind]

def getAnswers(ind):
    return answers[ind]

# copied from pymunk
def to_pygame(p, surface):
    """Convenience method to convert pymunk coordinates to pygame surface 
    local coordinates
    """
    return int(p[0]), surface.get_height()-int(p[1])

def distance(v1,v2):
    return math.sqrt( math.pow(v2[0]-v1[0],2) + math.pow(v2[1]-v1[1],2) )

def interpolate(v1, v2, r):
        return (v1[0] + (v2[0] - v1[0])*r, v1[1] + (v2[1] - v1[1])*r)

def vect_add(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

def vect_sub(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1])

def vect_mul(v,coeff):
    return (v[0]*coeff,v[1]*coeff)

def vect_norm(v):
    return math.sqrt( math.pow(v[0],2) + math.pow(v[1],2) )

def randomColor():
    return random.choice(["blue","red","yellow"])

def blockPlusOneAnim(color):
    if color == "blue":
        return plusOneAnimBlue.getCopy()
    elif color == "red":
        return plusOneAnimRed.getCopy()
    elif color == "yellow":
        return plusOneAnimYellow.getCopy()
