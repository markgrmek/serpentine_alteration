# Alteration of serpentine in the deep crust due to reactive fluid flow

This repository provides a finite difference solver and resources for simulating the reactive fluid flow occuring during the alteration of serpentine in the deep Earth's crust.

## Project Description

### Introduction

Fluid-rock interactions provide a link between chemical reactions and mass-energy transport. Understanting these proceses is critical for modeling hydrotermal ore deposit formations, carbon sequestration (carbon capture) and general rheological gravitational and magnetic changes in the litosphere. That being said, the timescales of these processes remain essentially unconstrained. However, analysing the alteration from serpentine to soapstone can expand our understanding, as it provides a good case study due to its clear reaction fronts and abundance of data.



## Running the Script

### Environment Setup

```
  python pip install requirements.txt
```

### Plotting the Equilibrium Thermodynamical Data
The equilibrium thermodynamic [data](data) was obtained with the helo of [Thermolab](https://hansjcv.github.io/Thermolab/)
The equilibrium thermodynamic plots are obtained by running [equilibrium_plotting.py](equilibrium_plotting.py) and are saved as .png in [figs](figs)

### Running the Simulation
1. The petrological parameters are found in [const.py](const.py)
2. The simulation is obtained by running [solver.py](solver.py). The simulation data is saved a .npz file in [output](output). Note that the simulation parameters are found at the beggining of the file
3. The animations of the reactive fluid flow are obtained by running [simulation_plotting.py](simulation_plotting.py). The animations are saved as .gif in [figs](figs)
