# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 07:24:05 2018

@author: DSA patterning the lazy way
"""

import numpy as np
import datetime
#%
Filename = datetime.datetime.now().strftime("%Y_%m%d_mdolejsi_DSACDBias")

ArH = 50*1e3
ArW = 50*1e3
ArSpace = 200*1e3
#base pitches
#base CD
BPArray = np.arange(76,96,2) #72-92
CDArray = BPArray/4*1.5 #target 1.5 L0
CDArray = CDArray + 10 #10 nm trim etch
CDArray = BPArray-CDArray # we're using a positive resist so we need to invert dims
CDArray = CDArray*0.7 # account for the fact at our best dose/develop we will expand the pattern CD
#round to nearest even
CDArray = np.round(CDArray/2,0)*2
#% X/Y spacing
BPos = np.arange(10)*ArSpace
xpos,ypos = np.meshgrid(BPos, BPos)
# Bias index
Bias = np.arange(-8,12,2)

ArrayWidth = np.arange(16,50,2)
#%% test
#This is needed to format the time properly. 
#GDS requires both time of creation and time of access
DTStr =  datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %m/%d/%Y %H:%M:%S \n")
#write header
with open(str(Filename+'.txt'), "w", newline='') as TextOut:
    TextOut.write("HEADER 600 \n")
    TextOut.write("BGNLIB "+DTStr)
    TextOut.write("LIBNAME LIB\n")
    TextOut.write("UNITS 0.001 1e-009 \n\n")
    for ii in ArrayWidth:
        TextOut.write("BGNSTR "+DTStr\
                      +"STRNAME %iw\n\n"%(ii)\
                      +"BOUNDARY \n"\
                      #set the layers
                      +"LAYER 1 \n"\
                      +"DATATYPE 0 \n"\
                      #define the box
                      +"XY 0: -%i\n"%(ArH/2)\
                      +"0: %i\n"%(ArH/2)\
                      +"%i: %i\n"%(ii,ArH/2)\
                      +"%i: -%i\n"%(ii,ArH/2)\
                      +"0: -%i\n"%(ArH/2)\
                      +"ENDEL \n"\
                      +"ENDSTR \n\n")
    # now write TOP
    TextOut.write("BGNSTR "+DTStr\
                  +"STRNAME TOP\n\n")
    #Now write the arrays 
    # How many pitches fit in the width?
    ColCnt = (ArW/BPArray).astype('int')
    for PitI in np.arange(BPArray.size): #for pitch index
        for BiasI in np.arange(Bias.size): # for a given bias
            BiasNeed = CDArray[PitI]+Bias[BiasI]
            TextOut.write("AREF \n"\
                          +"SNAME %iw\n"%BiasNeed\
                          +"COLROW %i 1 \n"%(ColCnt[PitI])\
                          +"XY %i: %i\n"%(BPos[PitI],BPos[BiasI])\
                          +"%i: %i\n"%(BPos[PitI]+BPArray[PitI]*ColCnt[PitI],BPos[BiasI])\
                          +"%i: %i\n"%(BPos[PitI],BPos[BiasI])\
                          +"ENDEL \n\n")                      
    #end top
    TextOut.write("ENDSTR \n")
    TextOut.write("ENDLIB \n")