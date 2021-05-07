# -*- coding: utf-8 -*-
"""NNs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nz47ZGxvwo4_jXV3j3gepnZjzzW-kJmH

## imports
"""

import torch
import torch.nn as nn
import random
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## Aux."""

def plot_accuracy(train_accuracies, train_losses, to_show = True, path_to_save = ''):
    
    train_len = len(np.array(train_accuracies))
    xs_train = list(range(0,train_len))
    
    
    plt.plot(xs_train, np.array(train_accuracies), label='Train Accuracy')
    plt.legend()
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.show()

    plt.plot(xs_train, np.array(train_losses), label='Train Losses')
    plt.legend()
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.show()

"""# Creating a simple network"""

# Defining sizes
input_size = 10
hidden_size = 5
output_size = 2
batch_size = 10

# Constructing the network
model = nn.Sequential(nn.Linear(input_size, hidden_size),
                     nn.Sigmoid(),
                     nn.Linear(hidden_size, output_size),
                     nn.Sigmoid())

# Let's work with some fake data
X = torch.randn(batch_size, input_size)
print(X)
y = torch.zeros(batch_size, output_size)
for i in range(0, y.size()[0]):
  y[i][random.randint(0, output_size-1)] = 1.0
print(y)

# define loss function
criterion = torch.nn.MSELoss()

# define the optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# and now let's train the model with the data that we created
# We use 1000 epochs

for epoch in range(1000):
    # Forward
    y_pred = model(X)
    
    # Compute and print loss
    loss = criterion(y_pred, y)
    print('epoch: ', epoch,' loss: ', loss.item())
    
    # Zero the gradients
    optimizer.zero_grad()
    
    # perform a backward pass (backpropagation)
    loss.backward()
    
    # Update the parameters
    optimizer.step()

"""# Creating a custom network"""

# Commented out IPython magic to ensure Python compatibility.
#load data from drive
from google.colab import drive
drive.mount('/content/drive')
# %cd /content/drive/My\ Drive/my_courses/deep_learning/fashion_mnist/

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        # fully connected layers
        self.fc1 = nn.Linear(784, 120) # 784 input dim (after flatten), 120 output channels 
        self.fc2 = nn.Linear(120, 84) # 120 input dim, 84 output channels 
        self.fc3 = nn.Linear(84, 10) # 84 input dim, 10 output channels 
        self.relu = nn.ReLU()

    def forward(self, x):
      x = torch.flatten(x, start_dim=1,end_dim=-1)
      x = self.fc1(x)
      x = self.relu(x)
      x = self.fc2(x)
      x = self.relu(x)
      x = self.fc3(x)
      
      return x

"""## Dataset and Dataloader

Dataset is an abstract class representing our dataset.

All datasets that represent a map from keys to data samples should subclass it. All subclasses should overwrite \__\__getitem\____(), supporting fetching a data sample for a given key. Subclasses could also optionally overwrite \__\__len\____(), which is expected to return the size of the dataset by many Sampler implementations and the default options of DataLoader.

we will use fashion mnist -https://github.com/zalandoresearch/fashion-mnist

![img](https://miro.medium.com/max/875/1*QQVbuP2SEasB0XAmvjW0AA.jpeg)

For most of the famous datasets we've got specific API in pytorch
"""

trainset = torchvision.datasets.FashionMNIST('F_MNIST_data/', download=True, train=True, transform=transforms.ToTensor())
trainloader = torch.utils.data.DataLoader(trainset, batch_size=16, shuffle=True)

testset = torchvision.datasets.FashionMNIST('F_MNIST_data/', download=True, train=False, transform=transforms.ToTensor())
testloader = torch.utils.data.DataLoader(testset, batch_size=16, shuffle=False)

# create a model
net = Net()
print(net)

# define loss function
criterion = nn.CrossEntropyLoss()

# define the optimizer
optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# training loop
losses = []
accs = []
print_every = 1000
for epoch in range(10):  
    runing_acc = 0.0
    running_loss = 0.0
    for i, data in enumerate(trainloader):
        
        # get the inputs
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward() #calculate all gradients
        optimizer.step()

        _, predicted = torch.max(outputs.data, 1)
        # print statistics
        running_loss += loss.item()
        runing_acc += accuracy_score(labels, predicted)*100
        if (i+1) % print_every == 0:    
          _loss = np.round(running_loss /print_every,3)
          _acc = np.round(runing_acc/print_every,3)
          losses.append(_loss)
          accs.append(_acc)
          print(f'Epoch: {epoch + 1}, Step: {i+1}, Loss: {str(_loss)}, Accuracy: {str(_acc)}')
          runing_acc = 0.0
          running_loss = 0.0

print('Finished Training')

plot_accuracy(accs, losses)

y_true = []
y_pred = []
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        y_true.extend(labels)
        _, predicted = torch.max(outputs.data, 1)
        y_pred.extend(predicted)


print(f'Accuracy of the network on the test images:{accuracy_score(y_true, y_pred)*100}%')

ind_to_label = {0:	'T-shirt/top',
                1:	'Trouser',
                2:	'Pullover',
                3:	'Dress',
                4:	'Coat',
                5:	'Sandal',
                6:	'Shirt',
                7:	'Sneaker',
                8:	'Bag',
                9:	'Ankle boot'}

for image, label, pred in zip(images, labels, predicted):
  print('====================================')
  print(f'True label: {ind_to_label[label.tolist()]}')
  print(f'Model prediction: {ind_to_label[pred.tolist()]}')
  plt.imshow(image.squeeze(), cmap='gray')
  plt.show()

