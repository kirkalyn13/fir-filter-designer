# FIR Filter Design Using the Window Function Method
# Reference: DSP Fundamentals and Applications by Tan and Jiang (p.288)
# Input Parameters:
# N: the number of FIR Filter taps (must be odd and minimum of 3)
# Fs: sampling frequency in Hz
# Ftype: the filter type
#    1. Lowpass filter
#    2. Highpass filter
#    3. Bandpass filter
#    4. Bandstop filter
# Wtype: the window type
#    1. Rectangular
#    2. Bartlett
#    3. Hanning
#    4. Hamming
#    5. Blackman
# WnL: lower cutoff frequency in radians.  Set WnL=0 for HPF.
# WnH: upper cutoff frequency in radians.  Set WnH=0 for LPF.
# Output:
# B: Designed FIR filter Coefficients

# matlab range | [start:step:stop]
# python range | range(start, stop, step)

# REVISION HISTORY
# REV    AUTHOR  COMMENT
# 0      JP      Initial version, graph for phase-freq response not identical to ma'am Beth sample

import numpy as np
from matplotlib import pyplot as plt
from operator import add
from operator import sub
from operator import mul
from operator import truediv
from scipy import signal

N = 51 #int(input('Desired # of filter taps(ODD) = '))
Fs= 3000 #float(input('Sampling Frequency in Hz = '))
Ftype = int(input('Filter Type #:[1]LPF [2]HPF [3]BPF [4]BSF= '))
WnL = 500 #float(input('Lower Cutoff Frequency in Hz(0 for HPF) = '))
WnH = 1000 #float(input('Higher Cutoff Frequency in Hz(0 for LPF) = '))
Wtype = int(input('Window Type #:[1]Rectangular [2]Bartlett [3]Hanning [4]Hamming [5]Blackman = '))
M=int((N-1)/2)
WnL=2*np.pi*WnL/Fs #1.0472
WnH=2*np.pi*WnH/Fs #2.0944

####### FOR HIGHER/UPPER CO FREQ #############
hHList=list(range(-M,0,1))
hH = []
#hH output 1x25
for x in range(M):
    lH = np.sin(WnH*hHList[x])/(hHList[x]*np.pi)
    hH.append(lH) 

#hH output 1x26
hH.append(WnH/np.pi)

#flip list and append flipped list to hH | 1x51
for x in reversed(range(M)):
    hH.append(hH[x])

######## FOR LOWER CO FREQ ############
hLList=list(range(-M,0,1))
hL = []
#hH output 1x25
for x in range(M):
    lL = np.sin(WnL*hLList[x])/(hLList[x]*np.pi)
    hL.append(lL) 

#hH output 1x26
hL.append(WnL/np.pi)

#flip list and append flipped list to hH | 1x51
for x in reversed(range(M)):
    hL.append(hL[x])

############## COMPUTE h ###############
h=[]
if Ftype == 1:
    h = hL
elif Ftype == 2:
    h = list(-1 * np.array(hH)) #1x51
    h[M] = 1+h[M] #update element 25
elif Ftype == 3:
    h = list(map(sub, hH, hL))
elif Ftype == 4:
    h = list(map(sub, hL, hH))
    h[M] = 1+h[M] #update element 25

############## COMPUTE w #############
w=[]
if Wtype == 1:
    w = list(np.ones(N))
elif Wtype == 2:
    x = list(range(-M,M+1,1))
    y = [M] *N 
    absList = list(map(abs,x))
    absL = list(map(truediv,absList,y))
    w = list(map(sub,list(np.ones(N)),absL))
elif Wtype == 3:
    x = list(range(-M,M+1,1))
    piList = [np.pi] *N
    y = list(map(mul,x,piList))
    z = [M] *N 
    piList2 = list(map(truediv,y,z))
    cosList = []
    for a in piList2:
        cosVal = np.cos(a)
        cosList.append(cosVal)  
    mpoint5List = [0.5] *N 
    mCosList = list(map(mul,mpoint5List,cosList))
    w = list(map(add,mpoint5List,mCosList))
elif Wtype == 4:
    x = list(range(-M,M+1,1))
    piList = [np.pi] *N
    y = list(map(mul,x,piList))
    z = [M] *N 
    piList2 = list(map(truediv,y,z))
    cosList = []
    for a in piList2:
        cosVal = np.cos(a)
        cosList.append(cosVal)  
    mpoint46List = [0.46] *N 
    apoint54List = [0.54] *N 
    mCosList = list(map(mul,mpoint46List,cosList))
    w = list(map(add,apoint54List,mCosList))
elif Wtype == 5:
    x = list(range(-M,M+1,1))
    piList = [np.pi] *N
    y = list(map(mul,x,piList))
    z = [M] *N 
    piList2 = list(map(truediv,y,z))#up to here reuse ok
    #cosList1
    cosList1 = []
    for a in piList2:
        cosVal1 = np.cos(a)
        cosList1.append(cosVal1)  
    mpoint5List = [0.5] *N 
    fCosList1 = list(map(mul,mpoint5List,cosList1))
    #cosList2
    cosList2 = []
    for a in piList2:
        cosVal2 = np.cos(2*a)
        cosList2.append(cosVal2)  
    mpoint08List = [0.08] *N 
    fCosList2 = list(map(mul,mpoint08List,cosList2))
    
    mpoint42List = [0.42] *N

    v = list(map(add,mpoint42List,fCosList1))
    w = list(map(add,v,fCosList2))

############ PLOT MAGNITUDE GRAPH ####################
#Designed Filter Coefficients
B = list(map(mul,h,w))
print("Designed Filter Coefficients = ", B)

#freqz function
fW, fH = signal.freqz(B)

#PLOTTING CONVERSION TO RAD AND DB
fig, axs = plt.subplots(2)
axs[0].set_title('Magnitude-Frequency Response')
axs[0].plot(fW/np.pi, 20 * np.log10(abs(fH)), 'b') #PLOT VALUE X
axs[0].set_ylabel('Amplitude [dB]', color='b')
axs[0].set_xlabel('Normalized Frequency [xπ rad/sample]')

angles = np.unwrap(np.angle(fH))
axs[1].set_title('Phase-Frequency Response')
axs[1].plot(fW/np.pi, angles*(180/np.pi), 'g') #PLOT VALUE Y
axs[1].set_ylabel('Phase (degrees)', color='g')
axs[1].grid(True)
axs[1].axis('tight')
axs[1].set_xlabel('Normalized Frequency [xπ rad/sample]')
plt.show()