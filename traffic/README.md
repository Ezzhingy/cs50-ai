# Traffic Experimentation

**Initial Setup**
My first attempt was simply to get the code working. I did not think about the number of layers nor types of layers to include in the neural network yet; I refered mostly to the lecture video when setting up the initial model. Below is what I ended up with:
- created a convolutional neural network
- added a convolutional layer, includes 32 3x3 filters with activation 'relu'
- added a max-pooling layer with a 2x2 pool size
- added a hidden layer with 128 units, with a dropout of 50%
- added an output layer with activation 'softmax'
These choices resulted in a final accuracy of 0.0564

**Final Setup after Experimentation**
After a bit of tinkering, I discovered a few things. Firstly, the main reason that the final accuracy was so low was due to the dropout factor. However, I still wanted to incorporate this dropout factor to prevent overfitting. To resolve this issue, I doubled the number of units in the hidden layer, which seemed to solve the problem. Furthermore, I added another convolution and pooling step to the model, which increased the final accuracy even more, since the neural network now has fewer, more specific and accurate inputs to work with. The final model is as follows:
- created a convolutional neural network
- added a convolutional layer, includes 32 3x3 filters with activation 'relu'
- added a max-pooling layer with a 2x2 pool size
- added another convolutional layer, includes 32 3x3 filters with activation 'relu'
- added another max-pooling layer with a 2x2 pool size
- added a hidden layer with 256 units, with a dropout of 50%
- added an output layer with activation 'softmax'
These choices resulted in a final accuracy of 0.9623

Trained using the German Traffic Sign Recognition Benchmark dataset, consisting of 26,640 images of 43 different kinds of roads signs
