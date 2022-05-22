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

LIST_SIZE = 32
batch = []
batches = []
redeemed = []
batchsize = 3
Current = []



class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.030 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLu:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
    
class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilites = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilites

class Input:
    def __init__(self, value) -> None:
        self.data = value
    def Set(self, inputs):
        self.data = inputs

    def assign(self, value):
        self.correct = value

    def DrawtoScreen(self):
        data = Shorten(self.data)
        canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
        for i in range(LIST_SIZE-1):
            canvas.create_line(data[i*2], data[i*2+1], data[i*2+2], data[i*2+3])
        canvas.create_line(data[(LIST_SIZE*2-1)-1], data[(LIST_SIZE*2-1)], data[0], data[1])

def Shorten(inputs):
    new = []
    x = math.floor(len(inputs)/LIST_SIZE)
    if x%2 != 0 : x -= 1
    for i in range(LIST_SIZE):
        new.append(float(inputs[x*i]))
        new.append(float(inputs[x*i+1]))
    return new.copy()


class Network:
    def __init__(self) -> None:
        self.layer1 = Layer_Dense(LIST_SIZE*2, 3)
        self.layer2 = Layer_Dense(3, 2)

        self.activation1 = Activation_ReLu()
        self.activation2 = Activation_Softmax()

    def set(self, layer1, layer2, activation1, activation2):
        self.layer1 = layer1
        self.layer2 = layer2
        self.activation1 = activation1
        self.activation2 = activation2



#class _Loss:
#    def calculate(self, output, y):
#        sample_losses = self.forward(output, y)
#        data_loss = np.mean(sample_losses)
#        return data_loss

#class _Loss_CategoricalCrossentropy(_Loss):
#    def forward(self, y_pred, y_true):
#        samples = len(y_pred)
#        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

#        if len(y_true.shape) == 1:
#            correct_confidences = y_pred_clipped[range(samples), y_true]
#        elif len(y_true.shape) == 2:
#            correct_confidences = np.sum(y_pred_clipped*y_true, axis = 1)

#        negative_log_likelihoods = -np.log(correct_confidences)
#        return negative_log_likelihoods


def Save(event):
    global inputs
    canvas.create_rectangle(0, 0, root.winfo_width(), root.winfo_height(), fill=bg_color, outline=bg_color)
    batch.append(Input(inputs.data.copy()))
    inputs = Input([])
    if len(batch) == batchsize:
        batches.append(batch.copy())
        batch.clear()

def Backpropagation(network, batch):
    Calculate(network, batch)

def Calculate(network, batch):
    if len(batch) > 0:
        network.layer1.forward(batch[0])
        network.activation1.forward(network.layer1.output)

        network.layer2.forward(network.activation1.output)
        network.activation2.forward(network.layer2.output)

        Calculated.append(network.activation2.output.copy())
        batch.remove(batch[0])

        print(network.activation2.output)
        Backpropagation(network, batch)
    else:
        root.unbind('0')
        root.unbind('1')
        exit()


def Generate_Button(button_title, command):
    global button
    button = Button(root, text=button_title, fg='blue', width=18, command=command)
    root.rowconfigure(1, pad=5)
    button.grid(row=1, column=0)

def Redeem_Batch():
    for i in range(0,3):
        batch[i] = Shorten(batch[i].data)
    redeemed.append(batch.copy())
    batches.pop()
    

def SetBatch():
    if len(batches)>0:
        global batch
        batch = batches[len(batches)-1].copy()        
    else:
        global Calculated
        Calculated = []
        network = Network()
        try:
            layer1 = open("layer1.txt", "r")
            layer2 = open("layer2.txt", "r")
            activation1 = open("activation1.txt", "r")
            activation2 = open("activation2.txt", "r") 
            network.set(layer1.read(), layer2.read(), activation1.read(), activation2.read())
        except:
            pass
        Calculate(network, redeemed)

def Assign_Zero(event):
    global root, i
    if i == 3 :
        Redeem_Batch()
        SetBatch()
        if len(batches)>0:
            i = 0
            batches[0][i].DrawtoScreen()
            batches[0][i].assign(0)
    else : 
        batches[0][i].DrawtoScreen()
        batches[0][i].assign(0)
        i += 1

def Assign_Full(event):
    global root, i
    if i == 3 :
        Redeem_Batch()
        SetBatch()
        if len(batches)>0:
            i = 0
            batches[0][i].DrawtoScreen()
            batches[0][i].assign(1)
    else : 
        batches[0][i].DrawtoScreen()
        batches[0][i].assign(1)
        i += 1


def Button1(event):
    global i
    SetBatch()
    batch[0].DrawtoScreen()
    button.grid_forget()
    root.unbind('<space>')
    i = 0
    root.bind('0', Assign_Zero)
    root.bind('1', Assign_Full)



def LineCreate(event):
    global Current
    Current = [event.x, event.y]
    inputs.data.append(Current[0])
    inputs.data.append(Current[1])

def LineUpdate(event):
    global Current
    canvas.create_line(Current[0], Current[1], event.x, event.y, fill='#000000', width=5)
    Current = [event.x, event.y]
    inputs.data.append(event.x)
    inputs.data.append(event.y)

Generate_Button('DO', lambda: Button1(None))
inputs = Input([])

canvas.bind('<1>', LineCreate)
canvas.bind('<B1-Motion>', LineUpdate)
root.bind('<space>', Save)

root.mainloop()
