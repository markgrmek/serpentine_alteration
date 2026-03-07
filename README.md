# Alteration of serpentine in the deep crust due to reactive fluid flow

This repository provides a finite difference solver and resources for simulating the reactive fluid flow occuring during the alteration of serpentine in the deep Earth's crust.


## Running the script

### Environment setup

```
  python pip install requirements.txt
```

### Plotting the equilibrium thermodynamical data
The equilibrium thermodynamic [data](data) was obtained with the helo of [Thermolab](https://hansjcv.github.io/Thermolab/)
The equilibrium thermodynamic plots are obtained by running [equilibrium_plotting.py](equilibrium_plotting.py) and are saved as .png in [figs](figs)

### Running the simulation
1. The petrological parameters are found in [const.py](const.py)
2. The simulation is obtained by running [solver.py](solver.py). The simulation data is saved a .npz file in [output](output). Note that the simulation parameters are found at the beggining of the file
3. The animations of the reactive fluid flow are obtained by running [simulation_plotting.py](simulation_plotting.py). The animations are saved as .gif in [figs](figs)
