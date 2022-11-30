# FIR Filter Designer
FIR Filter Designer App using Window Method written in Python.

## Installation
1. Download the .rar file from https://github.com/kirkalyn13/fir-filter-designer/releases/tag/v.1.0
2. Extract/Unzip the .rar file. It should produce a directory containing the "FilterDesigner.exe" file and other software files.

## Usage
Run the "FilterDesigner.exe" from the unzipped directory.

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
- Higher cutoff frequency in radians.  # Set to 0 for Low Pass Filter.

Output:
- Designed FIR Filter Coefficients
- Frequency Response Plot

## Authors
- Main Application: Engr. Kirk Alyn Santos
- Matlab to Python Conversion: Engr. Johannes Paulus de Guzman

## References
- DSP Fundamentals and Applications by Tan and Jiang (p.288)