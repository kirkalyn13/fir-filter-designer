# FIR Filter Designer

FIR Filter Designer App using Window Method written in Python.

## Installation
```
Download code zip file from Github repository.
```

## Usage
```python
## Run the Main Application File (main.py) in the code directory
python main.py
```

```
Input Parameters:
- Filter Types
   1. Lowpass filter
   2. Highpass filter
   3. Bandpass filter
   4. Bandstop filter
- Window Types
   1. Rectangular
   2. Bartlett
   3. Hanning
   4. Hamming
   5. Blackman
- Sampling frequency in Hz
- Number of FIR Filter taps.  # Must be odd and minimum of 3.
- Lower cutoff frequency in radians.  # Set to 0 for High Pass Filter.
- Higher cutoff: upper cutoff frequency in radians.  # Set to 0 for Low Pass Filter.
Output:
- Designed FIR filter Coefficients
- Frequency Response Plot
```

## Authors
```
Main Application: Engr. Kirk Alyn Santos
Matlab to Python Conversion: Engr. Johannes Paulus de Guzman
```

## Reference
```
DSP Fundamentals and Applications by Tan and Jiang (p.288)
```