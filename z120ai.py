import math
import numpy as np
from tkinter import *

bg_color = '#74E77A'

root = Tk()
root.title("Binary number reader")
root.geometry('333x400')
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
canvas = Canvas(root, bg=bg_color)
canvas.grid(row=0, column=0, sticky='nsew')

ListS = 32
batch = []
batchsize = 3
ButtonItter = 0
Current = []


class Input:
    def __init__(self) -> None:
        pass
    def Save(self):
        pass

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
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases



class Activation_ReLu:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
    
class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)



class Sample:
    def __init__(self) -> None:
        self.data = []
        self.dense1 = Layer_Dense(ListS*2, 3)
        self.dense2 = Layer_Dense(3, 2)

        self.activation1 = Activation_ReLu()
        self.activation2 = Activation_Softmax()

    def DrawtoScreen(self):
        canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
        for i in range(ListS-1):
            canvas.create_line(self.data[i*2], self.data[i*2+1], self.data[i*2+2], self.data[i*2+3])
        canvas.create_line(self.data[(ListS*2-1)-1], self.data[(ListS*2-1)], self.data[0], self.data[1])
    def Shorten(self):
        temp = []

        x = math.floor(len(self.data)/ListS)
        if x%2 != 0 : x -= 1
        for i in range(ListS):
            temp.append(float(self.data[x*i]))
            temp.append(float(self.data[x*i+1]))
        
        self.data = temp

    
    def write(self, value):
        self.data.append(value)


    def DoNeural(self, NotDebugging):
        if NotDebugging:
            root.destroy()
            self.Shorten()

        self.dense1.forward(self.data)
        self.activation1.forward(self.dense1.output)

        self.dense2.forward(self.activation1.output)
        self.activation2.forward(self.dense2.output)

        print(self.activation2.output)


    def DoBatchNeural(self, batch):
        root.destroy()

        self.dense1.forward(batch)
        self.activation1.forward(self.dense1.output)

        self.dense2.forward(self.activation1.output)
        self.activation2.forward(self.dense2.output)

        print(self.activation2.output)

 
def Debug(event):
    print(inputs.data)
    print(len(inputs.data))
    inputs.Shorten()
    inputs.DrawtoScreen()
    inputs.DoNeural(False)


def Batch(event):
    global inputs
    sampletap.grid_forget()
    debugtap.grid_forget()
    if len(inputs.data) >  0 :
        inputs.Shorten()
        batch.append(inputs.data)
        inputs = Sample()
    canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
    if (len(batch) == batchsize):
        inputs.DoBatchNeural(batch)



def LineCreate(event):
    global Current
    Current = [event.x, event.y]
    inputs.write(Current[0])
    inputs.write(Current[1])

def LineUpdate(event):
    global Current
    canvas.create_line(Current[0], Current[1], event.x, event.y, fill='#000000', width=5)
    Current = [event.x, event.y]
    inputs.data.append(event.x)
    inputs.data.append(event.y)


inputs = Sample()

sampletap = MyButton('sample', lambda: inputs.DoNeural(True), root)
sampletap.Place()
debugtap = MyButton('debug', lambda: Debug(None), root)
debugtap.Place()
batchtap = MyButton('batch', lambda: Batch(None), root)
batchtap.Place()

canvas.bind('<1>', LineCreate)
canvas.bind('<B1-Motion>', LineUpdate)
root.bind('<space>', Batch)

root.mainloop()
