import math
import numpy as np
from tkinter import *

Positions = []
Pos = []
V = [0, 0]
root_width, root_height = 333, 400
bg_color = '#74E77A'
ListS = 2
inputs = []
sample = []
batch = []
batchsize = 3
ButtonItter = 0
batching = False



class MyButton:
    def __init__(self, x_text, fn, root) -> None:
        self.x = Button(root, text=x_text, fg='blue', width=18, command=fn)
    
    def Place(self):
        global ButtonItter

        ButtonItter += 1
        root.rowconfigure(ButtonItter, pad=5)
        self.x.grid(row=ButtonItter, column=0)
    
    def grid_forget(self):
        self.x.grid_forget()
class Layer_Dense:
        def __init__(self, n_inputs, n_neurons):
            self.weights = np.random.randn(n_inputs, n_neurons)
            self.biases = np.zeros(n_neurons)
        def forward(self, inputs):
            self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLu:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities



def Shorten():
    inputs.clear()
    z=0
    Ratio = root.winfo_width()/root.winfo_height()
    if(Ratio<1):
        z=1
        Ratio = root.winfo_height()/root.winfo_width()
    
    x = math.floor(len(Positions)/ListS)
    if x%2 == 0 :
        for i in range(ListS):
            if(z==0):
                inputs.append((Positions[x*i]/root.winfo_width()*2-1))
                inputs.append((Positions[x*i+1]/root.winfo_height()*2-1)*Ratio)
            else:
                inputs.append((Positions[x*i]/root.winfo_width()*2-1)*Ratio)
                inputs.append((Positions[x*i+1]/root.winfo_height()*2-1))
    else:
        x -= 1
        for i in range(ListS):
            if(z==0):
                inputs.append((Positions[x*i]/root.winfo_width()*2-1))
                inputs.append((Positions[x*i+1]/root.winfo_height()*2-1)*Ratio)
            else:
                inputs.append((Positions[x*i]/root.winfo_width()*2-1)*Ratio)
                inputs.append((Positions[x*i+1]/root.winfo_height()*2-1))


def Sample(event):
    global batching, sample
    Shorten()
    sample = inputs
    batching = False
    Neural(sample, batch, batching)


def Debug(event):
    global batching, sample
    batching = False

    print(Positions)
    print(len(Positions))

    inputs.clear()
    x = math.floor(len(Positions)/ListS)
    if x%2 == 0 :
        for i in range(ListS):
            inputs.append(Positions[x*i])
            inputs.append(Positions[x*i+1])
    else:
        x -= 1
        for i in range(ListS):
            inputs.append(Positions[x*i])
            inputs.append(Positions[x*i+1])

    print(inputs)
    print(len(inputs))

    canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
    for i in range(ListS-1):
        i2=i*2
        canvas.create_line(inputs[i2], inputs[i2+1], inputs[i2+2], inputs[i2+3])
    canvas.create_line(inputs[(ListS*2-1)-1], inputs[(ListS*2-1)], inputs[0], inputs[1])

    Shorten()
    sample = inputs

    Neural(sample, batch, batching)


def Batch(event):
    global batch, batching, batchsize
    batching = True
    sampletap.grid_forget()
    debugtap.grid_forget()
    Shorten()
    batch.append(inputs.copy())
    canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
    if (len(batch) == batchsize):
        Neural(sample, batch, batching)


def locate_xy(event):
    global Pos
    Pos = [event.x, event.y]
    Positions.append(float(Pos[0]))
    Positions.append(float(Pos[1]))


def addLine(event):
    global Pos
    canvas.create_line(Pos[0], Pos[1], event.x, event.y, fill='#000000', width=5)
    Pos = [event.x, event.y]
    Positions.append(float(Pos[0]))
    Positions.append(float(Pos[1]))




def Neural():
    dense1 = Layer_Dense(2,3)
    activation1 = Activation_ReLu

    dense2 = Layer_Dense(3, 2)
    activation2 = Activation_Softmax()

    dense1.forward(inputs)
    activation1.forward(dense1.output)

    dense2.forward(activation1.output)
    activation2.forward(dense2.output)

    print(activation2.output[:5])




root = Tk()

root.title("Paint")
root.geometry((str(root_width) + 'x' + str(root_height)))

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

canvas = Canvas(root, bg=bg_color)
canvas.grid(row=0, column=0, sticky='nsew')


sampletap = MyButton('sample', lambda: Sample(None), root)
sampletap.Place()
debugtap = MyButton('debug', lambda: Debug(None), root)
debugtap.Place()
batchtap = MyButton('batch', lambda: Batch(None), root)
batchtap.Place()

canvas.bind('<1>', locate_xy)
canvas.bind('<B1-Motion>', addLine)

root.bind('<space>', Batch)

root.mainloop()
