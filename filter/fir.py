# FIR Filter Design Using the Window Function method
# Reference: DSP Fundamentals and Applications by Tan and Jiang (p.288)
# Input Parameters:
# N: the number of FIR Filter taps (must be odd and minimum of 3)
# sampling_frequency: sampling frequency in Hz
# filter_type: the filter type
#    1. Lowpass filter
#    2. Highpass filter
#    3. Bandpass filter
#    4. Bandstop filter
# window_type: the window type
#    1. Rectangular
#    2. Bartlett
#    3. Hanning
#    4. Hamming
#    5. Blackman
# lower_cutoff: lower cutoff frequency in radians.  Set lower_cutoff=0 for HPF.
# higher_cutoff: upper cutoff frequency in radians.  Set higher_cutoff=0 for LPF.
# Output:
# b: Designed FIR filter Coefficients

# matlab range | [start:step:stop]
# python range | range(start, stop, step)

# REVISION HISTORY
# REV    AUTHOR  COMMENT
# 0      JP      Initial version, graph for phase-freq response not identical to ma'am Beth sample

import numpy as np
from matplotlib import pyplot as plt
from operator import add, sub, mul, truediv
from scipy import signal

FILTERS = ["Low Pass", "High Pass", "Band Pass", "Band Stop"]
WINDOW_TYPES = ["Rectangular","Bartlett","Hanning","Hamming","Blackman"]

def window_method(filter_type, window_type, sampling_frequency, filter_taps, lower_cutoff, higher_cutoff):
    m = int((filter_taps-1)/2)
    lower_cutoff = 2*np.pi*lower_cutoff/sampling_frequency #1.0472
    higher_cutoff = 2*np.pi*higher_cutoff/sampling_frequency #2.0944

    ## FOR HIGHER/UPPER CO FREQ
    hh_list = list(range(-m,0,1))
    hh = []
    # hh output 1x25
    for x in range(m):
        lh = np.sin(higher_cutoff*hh_list[x])/(hh_list[x]*np.pi)
        hh.append(lh) 

    # hh output 1x26
    hh.append(higher_cutoff/np.pi)

    # Flip list and append flipped list to hh | 1x51
    for x in reversed(range(m)):
        hh.append(hh[x])

    ## FOR LOWER CO FREQ
    hl_list = list(range(-m,0,1))
    hl = []
    # hh output 1x25
    for x in range(m):
        ll = np.sin(lower_cutoff*hl_list[x])/(hl_list[x]*np.pi)
        hl.append(ll) 

    # hh output 1x26
    hl.append(lower_cutoff/np.pi)

    # Flip list and append flipped list to hh | 1x51
    for x in reversed(range(m)):
        hl.append(hl[x])

    ## COMPUTE h
    h = compute_h(filter_type, m, hl, hh)

    ## COMPUTE w
    w = compute_w(window_type, m, filter_taps)
    
    ## Plot Results
    plot_frequency_response(h, w)

## Compute for h 
def compute_h(filter_type, m, hl, hh):
    h = []
    if filter_type == "Low Pass":
        h = hl
    elif filter_type == "High Pass":
        h = list(-1 * np.array(hh)) #1x51
        h[m] = 1+h[m] #update element 25
    elif filter_type == "Band Pass":
        h = list(map(sub, hh, hl))
    elif filter_type == "Band Stop":
        h = list(map(sub, hl, hh))
        h[m] = 1+h[m] #update element 25
    return h

## Compute for w
def compute_w(window_type, m, filter_taps):
    w = []
    if window_type == "Rectangular":
        w = list(np.ones(filter_taps))
    elif window_type == "Bartlett":
        x = list(range(-m,m+1,1))
        y = [m] * filter_taps 
        abs_list = list(map(abs,x))
        abs_l = list(map(truediv,abs_list,y))
        w = list(map(sub,list(np.ones(filter_taps)),abs_l))
    elif window_type == "Hanning":
        x = list(range(-m,m+1,1))
        pi_list = [np.pi] * filter_taps
        y = list(map(mul,x,pi_list))
        z = [m] * filter_taps 
        pi_list2 = list(map(truediv,y,z))
        cos_list = []
        for a in pi_list2:
            cos_val = np.cos(a)
            cos_list.append(cos_val)  
        mpoint5_list = [0.5] * filter_taps 
        mcos_list = list(map(mul,mpoint5_list,cos_list))
        w = list(map(add,mpoint5_list,mcos_list))
    elif window_type == "Hamming":
        x = list(range(-m,m+1,1))
        pi_list = [np.pi] * filter_taps
        y = list(map(mul,x,pi_list))
        z = [m] * filter_taps 
        pi_list2 = list(map(truediv,y,z))
        cos_list = []
        for a in pi_list2:
            cos_val = np.cos(a)
            cos_list.append(cos_val)  
        mpoint46_list = [0.46] * filter_taps 
        apoint54_list = [0.54] * filter_taps 
        mcos_list = list(map(mul,mpoint46_list,cos_list))
        w = list(map(add,apoint54_list,mcos_list))
    elif window_type == "Blackman":
        x = list(range(-m,m+1,1))
        pi_list = [np.pi] * filter_taps
        y = list(map(mul,x,pi_list))
        z = [m] * filter_taps 
        pi_list2 = list(map(truediv,y,z))   #up to here reuse ok
        #cos_list1
        cos_list1 = []
        for a in pi_list2:
            cos_val1 = np.cos(a)
            cos_list1.append(cos_val1)  
        mpoint5_list = [0.5] * filter_taps
        f_cos_list1 = list(map(mul,mpoint5_list,cos_list1))
        #cos_list2
        cos_list2 = []
        for a in pi_list2:
            cos_val2 = np.cos(2*a)
            cos_list2.append(cos_val2)  
        mpoint08_list = [0.08] * filter_taps
        f_cos_list2 = list(map(mul,mpoint08_list,cos_list2))
        
        mpoint42_list = [0.42] * filter_taps

        v = list(map(add,mpoint42_list,f_cos_list1))
        w = list(map(add,v,f_cos_list2))

    return w

## PLOT MAGNITUDE GRAPH
def plot_frequency_response(h, w):
    # Designed Filter Coefficients
    b = list(map(mul,h,w))
    print("Designed Filter Coefficients = ", b)

    # freqz function
    fw, fh = signal.freqz(b)

    # PLOTTING CONVERSION TO RAD AND DB
    _, axs = plt.subplots(num="Frequency Response", ncols=2,figsize=(15, 5))
    axs[0].set_title('Magnitude-Frequency Response')
    axs[0].plot(fw/np.pi, 20 * np.log10(abs(fh)), 'b') #PLOT VALUE X
    axs[0].set_ylabel('Amplitude [dB]', color='b')
    axs[0].set_xlabel('Normalized Frequency [xπ rad/sample]')

    angles = np.unwrap(np.angle(fh))
    axs[1].set_title('Phase-Frequency Response')
    axs[1].plot(fw/np.pi, angles*(180/np.pi), 'g') #PLOT VALUE Y
    axs[1].set_ylabel('Phase (degrees)', color='g')
    axs[1].grid(True)
    axs[1].axis('tight')
    axs[1].set_xlabel('Normalized Frequency [xπ rad/sample]')
    plt.show()