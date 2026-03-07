# Alteration of serpentine in the deep crust due to reactive fluid flow

This repository provides a finite difference solver and resources for simulating the reactive fluid flow occuring during the alteration of serpentine in the deep Earth's crust.

## Project Description

### Introduction

Fluid-rock interactions provide a link between chemical reactions and mass-energy transport. Understanting these proceses is critical for modeling hydrotermal ore deposit formations, carbon sequestration (carbon capture) and general rheological gravitational and magnetic changes in the litosphere. That being said, the timescales of these processes remain essentially unconstrained. However, analysing the alteration from serpentine to soapstone can expand our understanding, as it provides a good case study due to its clear reaction fronts and abundance of data. This alteration is governed by the $\text{CO}_2$ dissolved in the fluid as such:

```math
\underbrace{2\text{Mg}_3\text{Si}_2\text{O}_5\text{(OH)}_4} _{\text{Serpentine}}
+ 3\text{CO} _{2,aq} 
\to
\underbrace{3\text{MgCO}_3} _{\text{Magnesite}}
+ \underbrace{\text{Mg}_3\text{Si}_4\text{O} _{10}\text{OH}_2} _{\text{Talc}}
+ 3\text{H}_2\text{0}
 \left( + \text{Chlorite} \right)
```

The main serpentine minerals are antigorite, chrysotile and lizardite, which are associated with ultramafic igneous rock formations. The petrological compositional space thus consists of $\text{SiO}_2$, $\text{Al}_2\text{O}_3$, $\text{MgO}$, $\text{FeO}$, $\text{Fe}_2\text{O}_3$  $\text{H}_2\text{O}$, $\text{CO}_2$ and $\text{CaO}$.

### Physical Background

The 1D alteration of serpentine can be described with the following advection-diffusion-reaction equation

```math
\frac{\partial}{\partial t}\left(\rho_f \phi + \rho_s(1-\phi)\right)
+
\frac{\partial}{\partial x}\left(\rho_f \phi v_f + \rho_s(1-\phi)v_s\right)
= 0
```

where $\rho_s$ and $\rho_f$ are the solids and fluid density respectivley, $\phi$ is the fluid saturation level and $v_s$ and $v_f$ are the solids and fluid velocities respectivley. Furthermore, the mass conservation of the immobile solid species is governed by:

```math
\frac{\partial}{\partial t}\left[\rho_s(1 - C_s^m)(1 - \phi)\right]
+
\frac{\partial}{\partial x}\left[\rho_s(1 - C_s^m)(1 - \phi)v_s\right]
= 0
```

where $C_s^m$ is the weight fraction of the mobile oxides, namely $\text{H}_2\text{O}$, $\text{CO}_2$ and $\text{SiO}_2$. Furthermore, the conservation of total $\text{CO}_2$ is enforced by satisfying:

```math
\frac{\partial}{\partial t}
\left[
\rho_f \phi C_f^{\text{CO}_2}
+
\rho_s (1-\phi) C_s^{\text{CO}_2}
\right]
+
\frac{\partial}{\partial x}
\left[
\rho_f \phi C_f^{\text{CO}_2} v_f
+
\rho_s (1-\phi) C_s^{\text{CO}_2} v_s
\right]
=
\frac{\partial}{\partial x}
\left[
\rho_f \phi D_f^{\text{CO}_2}
\frac{\partial C_f^{\text{CO}_2}}{\partial x}
\right]
```

where $C_f^{\text{CO}_2}$ and $C_s^{\text{CO}_2}$ are the maass fractions of $\text{CO}_2$ in fluids and solids, respectivley and $D_f^{\text{CO}_2}$ is the diffusion coefficient of $\text{CO}_2$ in the fluid. Lastly, the fluid flow can be described with Darcy's law (where the velocity of solids $v_s$ is assumed to be 0):

```math
\phi(v_f - v_s) = - \frac{k\phi^3}{\mu_f}\left(\frac{\partial p_f}{\partial x} + \rho_sg\right)
```

where $k$ is the permeability, $\mu_f$ is the dynamic viscosity of the fluid, $p_f$ is the fluid pressure and $g$ is the gravitational constant. The system of 3 unknowns is governed by 3 equations, making it solvalble, however it is very non-linear. For that reason a simple finite difference scheme was adopted according to [Beinlich et. al. 2020](https://www.nature.com/articles/s41561-020-0554-9)

### Methods

The thermodynamic equlibrium solid solution model was first assumed for 2 seperate Pressure and Temperature (PT) conditions, namely for low PT condiitons (0.3 GPa and 300°C, Beinlich et. al. 2020) and for high PT conditions (2.5 GPa and 800°C, Ota et. al. 2004). The two equilibrium thermodynamic models were then simulated in [Thermolab](https://hansjcv.github.io/Thermolab/) assuming the following oxide weight fractions (Beinlich et. al. 2020):

```math
\text{CaO}: 1.01\% ;
\quad
\text{SiO}_2: 40.08\% ;
\quad
\text{Al}_2\text{O}_3: 2.43\% ;
\quad
\text{MgO}: 34.97\% ;
\quad
\text{FeO}: 4.22\% ;
\quad
\text{Fe}_2\text{O}_3: 8.25\% ;
\quad
\text{H}_2\text{O}: 9.68\%
```

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
