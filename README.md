# HAMSTIR Driver

This is the robot-side code for implementing the 
[HAMSTIR](https://github.com/abefetterman/hamstir-gym) robot environments. The 
environments are designed to be run on the 
[AIY Vision Kit](https://aiyprojects.withgoogle.com/vision/), using the four 
outputs to drive two wheels with an H-Bridge.

To install, first update the SD Card from your AIY Vision Kit with the 
[latest release](https://github.com/google/aiyprojects-raspbian/releases).

Then follow the Vision Kit 
[connection guide](https://aiyprojects.withgoogle.com/vision/#connect) 
to connect to WiFi. 

SSH into your Raspberry Pi to clone the project (if you haven't yet,
  change the password!):
  
```
git clone https://github.com/abefetterman/hamstir-driver
cd hamstir-driver
```

Copy the model from your computer:

```
scp ./outgraph.bp pi@raspberrypi.local:~/
```

Then you can test the model on the raspberry pi with:

```
python3 ./hamstir-driver/test.py --model_path ./outgraph.bp
```

And run the model directly with:

```
python3 ./hamstir-driver/drive.py --model_path ./outgraph.bp
```