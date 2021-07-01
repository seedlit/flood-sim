# flood-sim

This repo is an extention of my other repo [sea-level-rise-sim](https://github.com/seedlit/sea-level-rise-sim). Along with DSM (Digital Surface Model), it also requires a corresponding ortho image.

### Example 1 - Under construction student housing at [IIT Gandhinagar](https://iitgn.ac.in/)
![Students Hostels](./results/iitgn_new_hostels_flood_sim.gif)
 #### Data:
I collected the data in 2019 using a DJI Phantom 3 Advanced. I used Agisoft PhotoScan to generate the ortho image and the DSM. However, a very good open source alternative is [Open Drone Map](https://github.com/OpenDroneMap/ODM). The ortho image (GSD = 1.8 cm) can be found [here](https://drive.google.com/file/d/1x9HuKJljVQoGFVORG5B76abeUclfz9Tb/view?usp=sharing), and the DSM (GSD = 3.6 cm) can be found [here](https://drive.google.com/file/d/1X1UeSfbJMC0CR4uSDQ_QGhxPonkqACdk/view?usp=sharing).

### Example 2 - Under construction Research Park at [IIT Gandhinagar](https://iitgn.ac.in/)
![Research Park](./results/iitgn_research_park.gif)

### Usage
Update the paramaters inside main.py and run main.py
