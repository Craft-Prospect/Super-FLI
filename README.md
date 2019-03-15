# **SUPER FLI -- Version 1.0**


**Overview:**

An arcade game where darknet's tiny-yolo convolutional neural network competes against the user to detect and destroy fires while dodging clouds to avoid losing health and orbiting the Earth. This Game can run on any Linux based operating system including the Raspberry Pi with joy stick and button peripherals or just your keyboard! All details are described below.


**Developers**

Team Project 3, Group ESE3 - 2018/19.

* Andrew Ritchie - 2253409r@student.gla.ac.uk - University of Glasgow
* Conor Begley   - 2236693b@student.gla.ac.uk - University of Glasgow
* Ibrahim Javed  - 2265799j@student.gla.ac.uk - University of Glasgow
* Vishrut Singh  - 2284553s@student.gla.ac.uk - University of Glasgow


***How to install***

*Note:*  We have two different installation guides below. The first if your using a laptop or PC with a Linux based operating system and the second for the Raspberry Pi 3.




**Laptop or PC**

*Requierments*

first, we need python3.6, to check if you already have it just use the following command.

```
python3.6 --version
```

If you dont, no need to worry just run the following.
```
sudo apt-get install python3.6
```

To run our network you need opencv. To do get this just run the following.
```
sudo apt-get install python-opencv
```

Now it's time to clone our project!

```
git clone "http://stgit.dcs.gla.ac.uk/tp3-2018-ese3/dissertation"
```

Once that's done move into our directory and we've provided a handy file which will install the rest of the requirements for you!
```
cd dissertation/
pip3 install -r requirements.txt
```

Now your good to go! Just jump down to the *how to run* section at the bottom to finish setup.




**Raspberry Pi**

*Requierments*

Our neural networks FPS (frames per second) on the raspberry pi was too slow for proper real-time detection. Therefore we outsource our neural processes to any computer system you have nearby over ethernet or even wirelessly. The following instructions show you how to set this up using an ethernet cable. To do this we need to enable SSH by inserting an empty file named "ssh" onto the boot partition of your Pi's SD card using another computer.

Now we need to update our pi and install python3.6, to do this on the Raspberry Pi use the following commands.
```
cd ~
sudo apt-get update
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
make -j4
sudo make altinstall
```

Next we need to install Python's arcade library
```
sudo apt install -y python3-dev python3-pip libjpeg-dev zlib1g-dev python-gst-1.0
sudo pip3.6 install arcade==1.3.7
```

Our final requierment is Python's library pygame. which is installed with the following commands.
```
cd ~
sudo apt-get install python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev \
libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev \
libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev

sudo apt-get install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame

python3.6 setup.py build
sudo python3.6 setup.py install
```

It's time to clone our repository!
```
git clone "http://stgit.dcs.gla.ac.uk/tp3-2018-ese3/dissertation"
```


Now we need to set up the computer that's going to handle our neural processes by sharing the Pi's public key from doing the following.

On your Pi check if you already have an existing SSH key pair. If you don't the command will output "file does not exist".
```
ls -al ~/.ssh/id_*.pub
```

If you do, you can skip the next two commands which are to generate a new SSH key pair.
```
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```
Once you've run the above command press Enter to accept the default file location and file name. Again just press Enter when you are prompted for a password. You should finally see the key's randomart image displayed.

To be sure that the SSH key was generated run
```
ls ~/.ssh/id_*
```

The output should look similar to this
```
/home/yourusername/.ssh/id_rsa /home/yourusername/.ssh/id_rsa.pub
```

Now we need to copy the Pi's public key to our remote machine. To do this we need to know the IP address of the remote machine. Log onto your remote machine and type "ifconfig" into the terminal. Your machines IP will be next to the label "inet" in the last group under the "UP,BROADCAST,RUNNING,MULTICAST" heading.


If you don't know the remote machines username just type "hostname" into its terminal. Now you can test the connection by running the following command on your Raspberry Pi.
```
ssh remote_username@server_ip_address's
```
If all the above commands were successful you should be asked for the server's password and then you will have full access to your server from the Raspberry Pi!

To finish close the terminal tab you used ssh on the Pi and re-open the terminal so your working on the Pi and use the following command.
```
cat ~/.ssh/id_rsa.pub | ssh remote_username@server_ip_address "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

Lets now test that we can remotely access your server without a password by trying to log in again from the Raspberry Pi.

```
ssh remote_username@server_ip_address
```

All going well you should not be prompted for a password!

Now you have to download a copy of the neural network on the remote server. To get a copy just clone our repository again on the server with the following command.
```
git clone "http://stgit.dcs.gla.ac.uk/tp3-2018-ese3/dissertation/"
```

We need to download the requirements on the server too. Don't worry you can do this by using the provided *requierments.txt* file.
```
cd dissertation/
pip3 install -r requirements.txt
```

To run our network you need opencv on the server. To do this just run the following.
```
sudo apt-get install python-opencv
```

Okay, you're nearly there, you just have to change a variable in your *constants.py* file located in **Game/** on the Pi. First, you need to uncomment the second COMMAND variable, don't worry about commenting out the other variable labelled COMMAND as it will be overwritten. You also need to uncomment the second RASP varible again dont worry about commenting the line above it.

Lastly, you need to edit the command you have just uncommented. Type in your hostname and IP_address of the server and add them into the second element of the list. Finally, on the server navigate into the yolo_tiny folder on the terminal and enter the command "pwd". Copy and paste the full output into the fourth element labelled "PWD_File_Path" in the example command.

**Example Command**
```
COMMAND = ['ssh', 'hostname@remote_IP_address', 'cd', 'PWD_File_Path', ';', './darknet', 'detector', 'test', 'cfg/obj.data', 'cfg/tiny-yolo.cfg', 'backup/tiny-yolo_2000.weights']
```

**Example pwd output**
```
/home/andrew/finished_code/dissertation/yolo_tiny
```

That's you all set up. To run the game see the section bellow.




**How to run**

Inside the cloned reposistory, run the following commands
```
cd Game
python3.6 run.py
```

The window will automatically pop up if your using a joystick make sure its plugged in before running the game.


Good Luck!

