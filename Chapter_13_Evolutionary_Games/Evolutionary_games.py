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

ccolor = ['#5429FF','#29A6FF','#29F7FF', '#29FFB0','#7BFF29','#D9FF29','#FFD429', '#FF2929']
ccolor = ccolor[::-1]


N = 7                             # Number of rounds 
L = 30                            # Lattice size
strategies = np.ceil(np.random.rand(L,L)*(N+1))-1


dynamic_mu = Scale(tk, from_=0, to=0.1, resolution = 0.001, orient=HORIZONTAL, label='Mutation probability')
dynamic_mu.place(relx=.5, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_mu.set(0.01)

dynamic_S = Scale(tk, from_=1, to=2, resolution=0.01 ,orient=HORIZONTAL, label='S')
dynamic_S.place(relx=.27, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_S.set(1.5)

dynamic_R = Scale(tk, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, label='R')
dynamic_R.place(relx=.05, rely=.84, relheight= 0.12, relwidth= 0.2)
dynamic_R.set(0.72)

def pd(R,S,N,n1,n2):                 
    # Prisoner's dilemma with two agents with strategies n1 and n2
    r = min(n1,n2)
    if n1<n2:
        p1 = r*R +(N-1-r)
        p2 = r*R + S + (N-1-r)
    elif n1 == n2:
        p1 = r*R + (N-r)
        p2 = p1
    else:
        p1 = r*R + S + (N-1-r)
        p2 = r*R + (N-1-r)
    return p1, p2

def mditer(strategies, R, S, N, L, mu):
    # Iterate through the lattice and update the strategies
    P = np.zeros((L,L))
    pind = np.roll(np.arange(L),-1)   # Index of the next element in the lattice
    mind = np.roll(np.arange(L),1)    # Index of the previous element in the lattice

    # play the game with the next neighbours and register points    
    for i in range(L):
        for j in range(L):
            p1, p2 = pd(R,S,N,strategies[i,j],strategies[pind[i],j])
            P[i,j] += p1
            P[pind[i],j] += p2

            p1, p2 = pd(R,S,N,strategies[i,j],strategies[i,pind[j]])
            P[i,j] += p1
            P[i,pind[j]] += p2

    newstrategies = np.zeros((L,L))

    for i in range(L):
        for j in range(L):
            if np.random.rand() < mu:    # mutate the strategy with probability mu
                newstrategies[i,j] = np.random.randint(N+1)  
            else:
                # copy the strategy of the neighbor with the lowest P, if P is equal, choose randomly
                pp = [P[i,j], P[mind[i],j], P[i,mind[j]], P[pind[i],j], P[i,pind[j]]]
                ss = [strategies[i,j], strategies[mind[i],j], strategies[i,mind[j]], strategies[pind[i],j], strategies[i,pind[j]]]
                newstrategies[i,j] = np.random.choice([ss[i] for i in range(5) if pp[i]==min(pp)])

    return newstrategies


def parameters_binary():
    global dynamic_mu, dynamic_S, dynamic_R, strategies, N, L, mu
    dynamic_mu.set(0)
    dynamic_S.set(1.5)
    dynamic_R.set(0.9)
    strategies = np.ones((L,L))*N
    strategies[int(L/2), int(L/2)] = 0

rest = Button(tk, text='Binary',command= parameters_binary) 
rest.place(relx=0.75, rely=.85, relheight= 0.12, relwidth= 0.15 )
evolutionary_games = np.uint8(np.zeros((L,L,3)))

while True:
    strategies = mditer(strategies, dynamic_R.get(), dynamic_S.get(), N, L, dynamic_mu.get())

    for i in range(L):
        for j in range(L):
            rgb = []
            for t in (1, 3, 5):
                rgb.append(int(ccolor[int(strategies[i,j])][t:t+2],16))

            evolutionary_games[i,j,:] = rgb

    
    img = itk.PhotoImage(Image.fromarray(np.uint8(evolutionary_games),'RGB').resize((res,res),resample=Image.BOX))
    canvas.create_image(0,0, anchor=NW, image=img) 
    tk.title('time'+ str(t) )
    time.sleep(0.01)
    tk.update()




                


