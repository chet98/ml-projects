import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

with open('GL Bot.json', 'r') as f:
     corpus = json.load(f)

print(corpus)
all_words=[]
tags=[]
xy=[]
for intent in corpus['intents']:
    tag=intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w=nltk.word_tokenize(pattern)
        all_words.extend(w)
        xy.append((w,tag))
ignore_words=['?','!',',','.']
all_words=[stem(w) for w in all_words if w not in ignore_words]
all_words=sorted(set(all_words))
tags=sorted(set(tags))
x_train=[]
y_train=[]
for(pattern_sentence,tag) in xy:
    bag= bag_of_words(pattern_sentence,all_words)
    x_train.append(bag)
    label=tags.index(tag)
    y_train.append(label)     #cross entrropy
x_train=np.array(x_train)
y_train=np.array(y_train)


class ChatDataset(Dataset):
        def _init_(self):
            self.n_samples = len(x_train)
            self.x_data = x_train
            self.y_data = y_train

        def _getitem_(self, index):
            return self.x_data[index], self.y_data[index]

        def _len_(self):
            return self.n_samples

batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(all_words)
learning_rate = 0.001
num_epochs = 1000
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size)
criterion=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=learning_rate)
for epoch in range(num_epochs):
    for (words,labels) in train_loader:
        words=words.to(device)
        labels=labels.to(device)

        outputs=model(words)
        loss=criterion(outputs,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if(epoch +1)%100==0:
        print(f'epoch{epoch+1}/{num_epochs},loss=loss={loss.item():.4f}')
print(f'final loss,loss={loss.item():.4f}')
data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
#this section of the code implements the code mentioned in nltk utils.py and model.py on x_train and y_train of the model and saves the model state, and input,output and hidden paramters in the FILE for further usage in the chotbot function
