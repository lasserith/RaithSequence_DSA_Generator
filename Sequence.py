# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 21:36:48 2018

@author: emosh
"""

import numpy as np

Filename = "Test"
BeamSS = 5 # beam step size nanometer
SubRes = 0.5 # subfield res in nanometer
SubF = 4.5 # subfield size in microns

Feature = "Lines"

#Feature = "Dots"
Dx = 150 # nanometers 
Dy = 150 # nanometers
#Feature = "Lines"
Width = 20 #nanometer
Pitch = 100 #nanometer

if Feature == "Dots":
    DxW = int(Dx/SubRes) # calculate in units of subfield res
    DyW = int(Dy/SubRes) # calculate in units of subfield res
    if (DxW != Dx/SubRes) or (DyW != Dy/SubRes):
        print('Dx and Dy are not divisors of subsize')
    
    XC = int(SubF*1000/Dx) # how many to fit in x
    YC = int(SubF*1000/Dy) # how many to fit in y
    with open(str(Filename+'.txt'), "w") as TextOut:
        for XX in np.arange(XC):        
            for YY in np.arange(YC): 
                if XX % 2 == 0: # go up
                    TextOut.write('sequence jump 0 {} reljmp \n'.format(DyW))
                else : #go down
                    TextOut.write('sequence jump 0 {} reljmp \n'.format(-DyW))
            TextOut.write('sequence jump {} {} reljmp \n'.format(DxW, DyW-DxW))
    
    
if Feature == "Lines":

    WidW = int(Width/BeamSS)
    PitW = int(Pitch/SubRes)
    
    XC = int(SubF*1000/Pitch) # how many lines
    YC = int(SubF*1000/BeamSS) # how many spots to go up
    with open(str(Filename+'.txt'), "w") as TextOut:
        for XX in np.arange(XC):        
            for YY in np.arange(YC): 
                
                if YY % 2 ==0: # go right
                    TextOut.write('\nsequence line X {}'.format(WidW))
                else: # or go left and then...
                    TextOut.write('\nsequence line X {}'.format(-WidW))
                if XX % 2 == 0: # go up or
                    TextOut.write('\nsequence line Y 1')
                else : #go down
                    TextOut.write('\nsequence line Y -1')
            # now at the top so lets jump to the right
            TextOut.write(' reljmp \nsequence jump {} 0'.format(PitW))
    
    
    