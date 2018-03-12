# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 21:36:48 2018

@author: emosh
"""

import numpy as np

Filename = "150nmSQDots45um"
BeamSS = 50 # beam step size nanometer
SubRes = 0.5 # subfield res in nanometer
SubF = 4.5 # subfield size in microns

Feature = "Dots"

#Feature = "Dots"
Dx = 150 # nanometers 
Dy = 150 # nanometers
#Feature = "Lines"
Width = 20 #nanometer
Pitch = 100 #nanometer


with open(str(Filename+'.txt'), "w") as TextOut:
	TextOut.write('BEAMER_GPF_Sequence_Definition\n\n')
	TextOut.write('SubFieldResolution {}\n'.format(SubRes/1000))
	TextOut.write('BeamStepSize {}\n\n'.format(SubRes/1000))
	TextOut.write('Replace Rect 0(0) {} {}\n'.format(SubF, SubF))
	TextOut.write('Sequence Offset X LSW 0\n')
	TextOut.write('Sequence Offset Y LSW 0\n')
    
	
	
if Feature == "Dots":
    DxW = int(Dx/SubRes) # calculate in units of subfield res
    DyW = int(Dy/SubRes) # calculate in units of subfield res
    if (DxW != Dx/SubRes) or (DyW != Dy/SubRes):
        print('Dx and Dy are not divisors of subsize')
    
    XC = int(SubF*1000/Dx) # how many to fit in x
    YC = int(SubF*1000/Dy) # how many to fit in y
    with open(str(Filename+'.txt'), "a") as TextOut:
        for XX in np.arange(XC):        
            for YY in np.arange(YC): 
                if XX + YY == 0: # if first time
                    TextOut.write('sequence lineclear X 1 reljmp \n')
                else:
                    if YY % 2 == 0: # go right
                        TextOut.write('sequence line X 1 reljmp \n')
                    if YY % 2 == 1: #go left
                        TextOut.write('sequence line X -1 reljmp \n')
                if XX % 2 == 0: # go up
                    TextOut.write('sequence jump 0 {} \n'.format(DyW))
                else : #go down
                    TextOut.write('sequence jump 0 {} \n'.format(-DyW))
            # if we are at the end of a column how do we jump to the next one?
            TextOut.write('sequence jump {} {} \n'.format(DxW, DyW-DxW))
    
    
if Feature == "Lines":

    WidW = int(Width/BeamSS)
    PitW = int(Pitch/SubRes)
    
    XC = int(SubF*1000/Pitch) # how many lines
    YC = int(SubF*1000/BeamSS) # how many spots to go up
    with open(str(Filename+'.txt'), "a") as TextOut:
        for XX in np.arange(XC):        
            for YY in np.arange(YC): 
                
                if YY % 2 ==0: # go right
                    if YY + XX == 0: # if first time
                        TextOut.write('\nsequence lineclear X {}'.format(WidW))
                    else: # go right
                        TextOut.write('\nsequence line X {}'.format(WidW))
                else: # or go left and then...
                    TextOut.write('\nsequence line X {}'.format(-WidW))
                if XX % 2 == 0: # go up or
                    TextOut.write('\nsequence line Y 1')
                else : #go down
                    TextOut.write('\nsequence line Y -1')
            # now at the top so lets jump to the right
            TextOut.write(' reljmp \nsequence jump {} 0'.format(PitW))
    
    
    