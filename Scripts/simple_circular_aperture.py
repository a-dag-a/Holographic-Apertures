import numpy as np

# Better to define the mask as a function
def apertureMask(vectorInput,polarInput=False):
    if polarInput==True:
        r = vectorInput[0]
        theta = vectorInput[1] # assuming theta in radians
    else:
        x = vectorInput[0]
        y = vectorInput[1]
        r = np.sqrt(x**2 + y**2)

        output = 1 if r<=1 else 0
    return output

# Construct an aperture function as an image
A = []

# Make sure M and N are odd numbers, so that there is a (0,0) pixel in the center
N = 1001
M = 1001

A = np.zeros((M,N))
coords_m = [(m-((M-1)/2))/(M/4) for m in range(M)]
coords_n = [(n-((N-1)/2))/(N/4) for n in range(N)]

for m in range(M):
    for n in range(N):
        A[m,n] = apertureMask((coords_m[m], coords_n[n]))

# Computing the FFT
F = np.zeros((M,N))
F = np.fft.fft2(A)

# Plotting
X,Y = np.meshgrid(coords_m,coords_n)
import matplotlib.pyplot as plt

f1 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X,Y,A)

F_magn = np.abs(F)
F_phase = np.angle(F)
f2 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X,Y,F_magn)
plt.xlabel('($k_x/(2\pi/M)$)')
plt.ylabel('($k_y/(2\pi/N)$)')
plt.show()

# Scan the mask, 
#     - detect the edge and its local normal. The local normal fixes the surviving polarization.
#     - Assign the surviving polarization to that pixel for the Greens function mask
# - Sum up vector Greens functions using the Greens function pixel mask.