# makeathon-autonomous-vehicle
A python project that lets you control a vehicle with a PS4 controller remotely that is written for Makeathon 2017 Case Competition in 36 hours

Details:
With a bluetooth dongle, PS4 controller is paired with BBB.
Manual mode (default):
R1, R2 controls right motor's forward and backward rotation
L1, L2 controls left motor's forward and backward rotation
Triangle lights up the headlights
Square goes into and out of autonomus mode
Autonomous mode:
Color sensors in the front left and right follow black tapes to stay in lane
Color sensors also keep a count of blue lines encountered to "know" where it is in the city.
IR sensor at the front of the car stops it if it encounters an obstacle
