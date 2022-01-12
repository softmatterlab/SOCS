import numpy as np 
from numpy import arctan2 as atan2, sin, cos
import matplotlib.pyplot as plt
from IPython import display
from scipy.constants import Boltzmann as kB 
from tkinter import *
from tkinter import ttk
from PIL import ImageGrab
import time

res = 500     # Resolution of the animation 
tk = Tk()
tk.geometry( str(int(res*1.1)) + 'x'  +  str(int(res*1.3)) )
tk.configure(background='white')

canvas = Canvas(tk, bd=2)            # Generate animation window 
tk.attributes('-topmost', 0)
canvas.place(x=res/20, y=res/20, height= res, width= res)
ccolor = ['#17888E', '#C1D02B', '#9E00C9', '#D80000', '#E87B00', '#9F68D3', '#4B934F']



dynamic_R = Scale(tk, from_=0, to=100, orient=HORIZONTAL, label='Aligning interaction range')
dynamic_R.place(relx=.5, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_R.set(10)

dynamic_Dr = Scale(tk, from_=0, to=1, resolution=0.01 ,orient=HORIZONTAL, label='Rotational diffusion strength')
dynamic_Dr.place(relx=.27, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_Dr.set(0.1)

dynamic_n = Scale(tk, from_=1, to=100, orient=HORIZONTAL, label='Number of particles')
dynamic_n.place(relx=.05, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_n.set(50)


# Parameters of the simulation
n = dynamic_n.get()     # Number of particles 
N = 100000  # Simulation time
dt = 0.03   # Time step 

# Physical parameters of the system 
l = 100
V = 20         # Particle velocity 
R = 4


x = np.random.rand(n)*2*l - l    # x coordinates            
y = np.random.rand(n)*2*l - l    # y coordinates  
phi = np.random.rand(n)*2*np.pi  # orientations                # Initialization 

particles = []
for j in range(n):     # Generate animated particles in Canvas 
    
    particles.append( canvas.create_oval( (x[j]-R + l)*res/l/2, \
                                          (y[j]-R + l)*res/2/l, \
                                          (x[j]+R + l)*res/l/2, \
                                          (y[j]+R + l)*res/l/2, \
                                          outline=ccolor[0], fill=ccolor[0]) )
for i in range(N):
    rad = dynamic_R.get()
    Dr = dynamic_Dr.get()
    n  = dynamic_n.get()
    
    if n > len(x):
        x = np.append(x,  np.random.rand(n-len(x))*2*l - l)
        y = np.append(y,  np.random.rand(n-len(y))*2*l - l)
        phi = np.append(phi, np.random.rand(n-len(phi))*2*np.pi)
        for j in range(len(particles),n):
            particles.append( canvas.create_oval( (x[j]-R + l)*res/l/2, \
                                          (y[j]-R + l)*res/2/l, \
                                          (x[j]+R + l)*res/l/2, \
                                          (y[j]+R + l)*res/l/2, \
                                          outline=ccolor[0], fill=ccolor[0]) )
        
    if n < len(x):
        for j in range(n,len(x)):
            canvas.delete(particles[j])
        x = x[:n]
        y = y[:n]
        phi = phi[:n]
        particles = particles[:n]
        
    
    x = (x + V*cos(phi)*dt +l) % (2*l) - l    # Update x coordinates
    y = (y + V*sin(phi)*dt +l) % (2*l) - l    # Update y coordinates
    
    clustering = np.zeros(n)
    for j in range(n):
        distances = np.sqrt((x-x[j])**2 + (y-y[j])**2)      # Calculate distances array to the particle       
        interact = distances < rad                          # Create interaction indices 
        phi[j] = np.angle(np.sum(np.exp(phi[interact]*1j))) + Dr * np.random.randn()                                   # Update orientations

                
    for j in range(n):
        canvas.coords(particles[j], 
                      (x[j]-R + l)*res/l/2, \
                      (y[j]-R + l)*res/2/l, \
                      (x[j]+R + l)*res/l/2, \
                      (y[j]+R + l)*res/l/2,)     # Updating animation coordinates 
    tk.title('t =' + str(round(i*dt*100)/100))          # Animation title 
    tk.update()                                         # Update animation frame 
    time.sleep(0.01)                                     # Wait between loops
    
Tk.mainloop(canvas)                                     # Release animation handle (close window to finish)