#Python and SensHat Programming (RMIT_IOT_Assignment1)


# IOT_Assignment1
IOT A_1 s3667340,s3699505

#Files 
1-MonitorandNotify.py 
2-CreateReport.py 
3-greenHouse_bluetooth.py     (https://github.com/Azelphur/pyPushBullet)
4- Analytics.py

# 1- Getting Started
- clone or copy the repostories to your local machine 


#2- Prerequisites
-This  code was written to be run on PI model (Raspberry Pi 3 Model B) for more info https://au.element14.com/element14/pi3-ibm-iot-learnkit/raspberry-pi-3-ibm-iot-learner/dp/2606882
- You need to have a working senhat model attached to your pi
- we used python version 3 
- For analytics ,pandas , matplotlib , Seaborn, Pygal
- follow section 3 to install dependencies 
#Dependencies and application
- Sqlite3 
- SQLDBBrowser
- sensehat 
- jason 
- in bulit (os python package relative path )
- bluetooth library ,Pybluez ,pyPushbullet 


#3- Raspberry Pi dependencies to install 
- update & install senseHat
   *** sudo apt-get install sense-hat ***
- for python3 dependencies  ( ***sudo apt-get Instal pip3***)
- *** sudo apt-get install sqlite3*** (in terminal type *** sqlite3 *** to launch in terminal)
- If you prefer gui represtantion of your tables in database install SQliteBrowser  ***https://sqlitebrowser.org/***
- In order to use pi bluetooth u need to install the following:
  - Pybluez 
    - ( ***sudo apt-get install bluetooth libbluetooth-dev ***)
    - ( ***sudo pip3 install pybluez**)
- For Analytics install the following 
    - for data manuplation pandas( ***pip3 install pandas*** ) 
    - for data visualization:
        matplotlib ,Seaborn dependecy (***pip3 install matplotlib***) install on client ssh as well 
        Seaborn for histogram ( ***pip3 install Seaborn***)
        Pygal for scatterplot ( ***pip3 install pygal**)
 - For PushBullet 
 - Create your account on https://www.pushbullet.com/
 - register your device with exact name as your device's bluetooth name (in this code we are matching device nickname with bluetooth name)
 - install pyPushbullet library from  (https://github.com/Azelphur/pyPushBullet)  


# Authors
- Sarvatra Indoria (s3699505) 
- Yamin Huzaifa (s3667340)

# References and Acknowledgement 
- Temperature computation (http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html)
- Python plotting libraries (https://mode.com/blog/python-data-visualization-libraries)
- Pushbullet library (https://github.com/Azelphur/pyPushBullet)
- for CronJob on pi follow (https://crontab.guru/)


      
      
      
     ****May The Force Be With You***