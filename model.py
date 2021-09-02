# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and se

import torch
import torch.nn as nn

class NeuralNet(nn.Module):
        def _init_(self, input_size, hidden_size, num_classes):
            super(NeuralNet, self)._init_()
            self.l1 = nn.linear(input_size,hidden_size)
            self.l2 = nn.linear(hidden_size,hidden_size)
            self.l3 = nn.linear(hidden_size,num_classes)
            self.relu = nn.ReLU()
        def forward(self, x):
            out= self.l1(x)
            out= self.relu(out)
            out= self.l2(x)
            out= self.relu(out)
            out= self.l3(x)
            return out
#The main fucntion of this code is to define the model for the neural net structure that defined the feed forward neural network