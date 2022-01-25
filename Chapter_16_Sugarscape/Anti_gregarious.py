import numpy as np 
from numpy import arctan2 as atan2, sin, cos
import matplotlib.pyplot as plt
from IPython import display
from scipy.constants import Boltzmann as kB 
from tkinter import *
from tkinter import ttk
from PIL import ImageGrab
from PIL import Image
from PIL import ImageTk as itk
import time

res = 500     # Resolution of the animation 
tk = Tk()
tk.geometry( str(int(res*1.1)) + 'x'  +  str(int(res*1.3)) )
tk.configure(background='white')

canvas = Canvas(tk, bd=2)            # Generate animation window 
tk.attributes('-topmost', 0)
canvas.place(x=res/20, y=res/20, height= res, width= res)

ccolor = ['#FFDB44', '#CB5D19']

# Initialize the lattice
def init_lattice(N=50):                # Size of the lattice
    global S
    S = np.zeros((N,N))
    n = int(0.9*N**2)                      # Number of agents
    # half of the agents will be in family A, the other half in family B
    indices_initial = np.random.choice(np.arange(N**2), int(n), replace=False)
    indices_A = [indices_initial[:int(n/2)]//N, indices_initial[:int(n/2)]%N]
    indices_B = [indices_initial[int(n/2):]//N, indices_initial[int(n/2):]%N]
    S[indices_A] = 1         # place family A agents (represented by 1)
    S[indices_B] = -1         # place family B agents (represented by -1)


rest = Button(tk, text='Restart',command= init_lattice) 
rest.place(relx=0.15, rely=.85, relheight= 0.12, relwidth= 0.7 )

N = 50
init_lattice(N)
sugarscape = np.uint8(np.ones((N,N,3))*255)

while True:
    # Choose a lattice site randomly that is not zero
    while True:
        x = np.random.randint(0,N)
        y = np.random.randint(0,N)
        if S[x,y] != 0 and x>0 and y>0 and x<N-1 and y<N-1:
            break
    # check if the family is happy or not
    if np.sign(S[x,y]) == np.sign(sum(sum(S[x-1:x+2,y-1:y+2]))) or sum(sum(S[x-1:x+2,y-1:y+2])) == 0:
        # if not happy, choose a random neighbor that is zero
        while True:
            x_new = np.random.randint(0,N)
            y_new = np.random.randint(0,N)
            if S[x_new,y_new] == 0:
                break
        # if the neighbor is zero, move the agent
        S[x_new,y_new] = S[x,y]
        S[x,y] = 0    

    # update the sugarscape
    for i in range(N):
        for j in range(N):
            if S[i,j] == 1:    
                rgb = []
                for t in (1, 3, 5):
                    rgb.append(int(ccolor[0][t:t+2],16))
                sugarscape[i,j,:] = rgb 
            elif S[i,j] == -1:
                rgb = []
                for t in (1, 3, 5):
                    rgb.append(int(ccolor[1][t:t+2],16))
                sugarscape[i, j, :] = rgb
            else:
                sugarscape[i, j, :] = [255, 255, 255]

    img = itk.PhotoImage(Image.fromarray(sugarscape,'RGB').resize((res,res),resample=Image.BOX))
    canvas.create_image(0,0, anchor=NW, image=img) 
    time.sleep(0.01)
    tk.update()




                


