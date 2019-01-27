Neural Network Description

COMMITS
The full NN will not be able to be pushed to gitlad until it is fully working. 
This is due to the base network alreadying being on the git system and it seems to create bugs. 
In saying that the errors are due to requierments and training and once this has been sorted a 
full decription file will be added.

Neural Network
The network is provided by darknet. It is a convolutional network that has some provided weights. 
Team ESE3 is curently training an object detection weight to identify fires, this testing will 
start on Monday the 27th of Jan as all the equipment (GPU's) has now been set up.

System Integration
The NN will run seprate to the game with one link in the form of the captured screen shots provided
by the game and located in the data file. As the screen shots are taken the network will look at the
file and return 4 numbers representing the coordinates of the fires location at the time of the screen
shot. Speed is a major factor for the networks accuracy and we are currently working on 2 base networks
with one that sacrifices preformance for speed as a back up network.
