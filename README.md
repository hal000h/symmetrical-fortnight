## Code snippets useful for debugging
```
raise Exception() # prevents python from executing the code below this line. this let you try just 1 HDB, Mission pad or  QR code first.
```
## Combat drone drifting
The longer the drone flies, the more inaccurate its positioning/movement becomes.

This is because when you command the drone to say move forward 1m, it knows when to stop by tracking how far it has moved. It does so by integrating the forward acceleration detected by its IMU (inertial measurement unit) sensor twice.

If this sounds odd, remember from physics that integrating acceleration/time graph gets you velocity/time graph, and integrating velocity/time graph gets you distance/time graph.

IMU is a very sensitive sensor but also has high random error. This error accumulates over time. As a result, the drone's positioning becomes more inaccurate the longer it flies.

To combat this, after each HDB/QR code, go to a nearby mission pad, and run `align_to_mission_pad()`. this realigns the drone to the center of the grid.
