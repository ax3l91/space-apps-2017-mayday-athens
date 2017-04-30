# Space Apps Challenge: Mayday, Mayday, Mayday!

Prototype application in Python which calculates and visualizes the radiation a crew member or passenger will receive in a polar or near-polar flight. It takes into consideration our analysis, of how solar energetic particles and cosmic rays dynamically interact with earth's magnetic field and atmosphere, explained in the documentation [MaydayMaydayMayday.pdf].

# Simulation
The simulation is being done in [Kp.ipynb] which:

Requires Input:
  - Kp Index
  - Flight Route
  - GOES Satellite FLux Data
  - Aurora Prediction Data (For Display Use Only)

Provides Output:
- Total Radiation Dose For An Average Human
- Time Series Of Exposure During The Flight
- Physical Simulation in 3D World Model

# Visualization
The visualization given at [Kp.ipynb] provides a first level of visualization. The [index.html] file provides a front end that pulls the simulation data and visualizes them in a user friendly way.

The visualization in the html file is split in four parts.
  - 3D visualization of the globe with the simulated flight path pseudo-colored according to the radiation intensity at each point.
  - 2D visualization of the world map marking the flight path and showing the expected aurora probability at each point.
  - Live chart of the cumulative radiation dose of the flight path to the distance traveled. The user can hover over the line of the chart to get exact values of time and total radiation dose value for a point in time.
  - Total radiation dosage and generated comments on the health aspects of the simulated flight in an. understandable way for the general public with examples out of the everyday life.
  
In order to create the web application the following libraries were used:
* [X3dom] - 3D javascript Library
* [Rickshaw] - A Javascript Toolkit for creating interactive graphs

### Installation

If you want to run the [Kp.ipynb] calculation outside of github you will need the following python modules:
- aacgmv2
- basemap

Additionally the script requires GNU/Wget in order to download current NASA data.

   [X3dom]: <https://www.x3dom.org/>
   [Rickshaw]: <https://github.com/shutterstock/rickshaw>
   [Kp.ipynb]: <https://github.com/ax3l91/space-apps-2017-mayday-athens/blob/master/Kp.ipynb>
   [index.html]: <https://github.com/ax3l91/space-apps-2017-mayday-athens/blob/master/index.html>
   [MaydayMaydayMayday.pdf]: <https://github.com/ax3l91/space-apps-2017-mayday-athens/blob/master/MaydayMaydayMayday.pdf>
