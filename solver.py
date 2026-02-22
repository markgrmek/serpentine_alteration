import numpy as np
from const import *
from utils import pair_avg, create_solver_interpolators, absmax

#GENERAL SOLVER PARAMS----------------------------------------------------------
PTtype: str = 'lowPT'
npow: int = 3 #non linearity in permeability
N_sweeps: int = int(1e5) #number of sweeps
N_Pf_max: int = int(1e4) #maximum number of fluid pressure sweeps
tolerance: float = 1e-6 #tolerance of approximation
interp = create_solver_interpolators(PTtype)

#DOMAIN-------------------------------------------------------------------------
L: float = 1.0 #domain length (m)
N_cells: int = 200 #number of cells
x: np.ndarray  = np.linspace(0, L, N_cells+1) #discrete domain
dx: float = L/N_cells  #step in x (m)
pres: float = P[PTtype]

#TIME---------------------------------------------------------------------------
time_tot: float = 0.002 #100*L**2/DCO2_B #total integration time (s)
N_steps: int = int(1e9) #number of time steps
N_steps_in_epoch: int = 100 #results get stored per each epoch

#INITIAL CONDITIONS-------------------------------------------------------------
por0: np.ndarray = np.full(N_cells, POR_B) #initial porosity
P_fl0: np.ndarray = np.linspace(pres, 0, N_cells) #initial fluid pressure gradient (from P_0 to 0 as x from 0 to L)
wCO2_s0: np.ndarray = np.full(N_cells, WCO2_B) #initial CO2 fluid (the rest serpentine)
wCO2_s0[0] = WCO2_SOAP #first cell is soapstone

#CREATE OUTPUT DICTIONARY-------------------------------------------------------
interp_outputs = {col: [] for col in INTERP_MAP.keys() if col in interp.keys()} #the interpolation vars that overlap
noninterp_outputs = {col: [] for col in NONINTERP_MAP.keys()}


print(':::STARTED SIMULAITON:::')
#PLACE HOLDERS
wCO2_s = wCO2_s0.copy()
P_fl = P_fl0.copy()
por_rho_s_wMg0 = None #mass of immobile species at t=0
rho_tot_prev = None #total density at previous time step

time = 0
for time_step in range(N_steps):
    
    #CALC VARS WITH INTERPOLATION--------------------------------------------
    rho_s  = interp['rho_s'](wCO2_s)
    rho_fl = interp['rho_fl'](wCO2_s)
    wCO2_fl = interp['wCO2_fl'](wCO2_s)
    wMg_s = interp['wMg_s'](wCO2_s)
    mu_fl = interp['mu_fl'](wCO2_s)

    #CALCULATE IMMOBILE SPECIES DENSITY--------------------------------------
    if time_step == 0: 
        por_rho_s_wMg0 = rho_s * wMg_s * (1-por0) #store initial value

    rho_im = rho_s * wMg_s #calculate imobile species density
    por = 1 - por_rho_s_wMg0 / rho_im #calulcate porosity
    rho_tot = rho_fl * por + rho_s * (1-por) #calulcate total density

    if time_step == 0:
        rho_tot_prev = rho_tot #store initial value

    rho_CO2_tot = rho_fl * por * wCO2_fl + rho_s * wCO2_s * (1-por) #calculate total rho CO2

    #AVERAGE VALUES ON INTERFACES BETWEEN NODES--------------------------------
    rho_fl_avg = pair_avg(rho_fl) #density of fluid
    rho_CO2_fl_avg = rho_fl * wCO2_fl
    rho_CO2_fl_avg = pair_avg(rho_CO2_fl_avg) #density of CO2_fl in the system
    por_avg = pair_avg(por) #porosity
    perm_avg = KMUF_B * por_avg**npow  #permeability
    dCO2_avg = rho_CO2_fl_avg * por_avg * DCO2_B #diffusivity

    #PRESSURE SWEEPS-------------------------------------------------------------
    rho_tot_delta = rho_tot[1:-1]-rho_tot_prev[1:-1]
    for sweep in range(N_sweeps):
        P_grad = np.diff(P_fl) / dx #calculate pressure gradient in x

        #DEFINE PROPER TIME STEP--------------------------------------------------
        dt_diff = 0.45 * dx**2 / DCO2_B #calulate max time step for diffusion
        dt_adv = rho_fl_avg * perm_avg * P_grad
        dt_adv = 0.45 * dx / absmax(dt_adv) #calulate max time step for advection
        time_remain = time_tot - time #calculate remaining time
        dt = np.min((dt_diff, dt_adv, time_remain)) #we use whicever timestep is smaller to achieve stability

        #dt is the bottle neck 
        if dt == 0.0 and time_remain == 0.0: #end of simulation
            break
        
        elif dt == 0.0 and time_remain > 0.0: #dt is 0 but we are not at the end
            raise ValueError('dt is 0')

        #CALCULATE DARY FLUX--------------------------------------------------------
        flux = - perm_avg * P_grad

        #CALC THE RESIDUAL PRES. OF TOTAL MASS BALANCE AND UPDATE PRES.
        #(leave out outermost cells <-> BC)
        P_res = - rho_tot_delta / dt - np.diff(rho_fl_avg * flux) / dx #this term should ideally be 0
        sweep_calc = (P_res *dx**2) / (np.max(perm_avg * rho_fl_avg) * 4)
        P_fl[1:-1] = P_fl[1:-1] + sweep_calc

        if absmax(P_res) <= tolerance: #break when the pressure is sufficiently swept
            break

        if sweep == N_sweeps:
            raise ValueError('Pressure sweeping failed. Adjust parameters')
    
    #DIFFUSIVITY FLUX-------------------------------------------------------------
    diff_flux = - dCO2_avg * np.diff(mu_fl) / dx

    #ADJUST THE MASS FRAC. OF CO2 IN THE SYSTEM
    # leave out the boundary conditions (leftmost is already soapstone, rightmost stays serpentine)
    rho_CO2_tot_itm = diff_flux + rho_CO2_fl_avg * flux
    rho_CO2_tot_itm = np.diff(rho_CO2_tot_itm)
    rho_CO2_tot[1:-1] = rho_CO2_tot[1:-1] - dt * rho_CO2_tot_itm / dx

    #CALC NEW CO2 IN FLUID VAL. FROM BALANCE EQ.
    wCO2_s = (rho_CO2_tot - wCO2_fl * rho_fl * por)/(rho_s * (1-por))

    #UPDATE VALUES-----------------------------------------------------------------
    rho_tot_prev = rho_tot
    time += dt

    #P_fl gets update inside the loop
    #wCO2_s gets updated at the end
    #rho_im0 gets updated just in the first iteration (rho_im at t=0)
   
    #PRINT RESULTS-----------------------------------------------------------------
    if time_step % N_steps_in_epoch == 0: #print out result of each time step
        print(f"""
            =========================================================================
            :::TIMESTEP: {time_step} => TIME: {time}s of {time_tot}s:::
            =========================================================================
            Domain: {x[0]:.2e}, {x[1]:.2e} ... {x[-2]:.2e},{x[-1]:.2e};
            Fluid pressure: {P_fl[0]:.2e}, {P_fl[1]:.2e} ... {P_fl[-2]:.2e}, {P_fl[-1]:.2e};
            CO2 in solids: {wCO2_s[0]:.2e}, {wCO2_s[1]:.2e} ... {wCO2_s[-2]:.2e}, {wCO2_s[-1]:.2e};
            Porosity: {por[0]:.2e}, {por[1]:.2e} ... {por[-2]:.2e}, {por[-1]:.2e};
            Permeability: {perm_avg[0]:.2e}, {perm_avg[1]:.2e} ... {perm_avg[-2]:.2e}, {perm_avg[-1]:.2e};
            CO2 diffusivity: {dCO2_avg[0]:.2e}, {dCO2_avg[1]:.2e} ... {dCO2_avg[-2]:.2e}, {dCO2_avg[-1]:.2e};
            """
        )
        
        print('storing results...')


        #APPEND RESULTS------------------------------------------------------------
            # calculated (non-interpolted) variables
        noninterp_outputs['time'].append(time)
        noninterp_outputs['wCO2_s'].append(wCO2_s)
        noninterp_outputs['wCO2_fl'].append(wCO2_fl)
        noninterp_outputs['por'].append(por)
        noninterp_outputs['rho_tot'].append(rho_tot)

            # interpolated variables
        for key in interp_outputs.keys():
            interp_outputs[key].append(interp[key](wCO2_s))

        print('results stored. Simulating next epoch...')

    #SAVE RESULTS--------------------------------------------------------------------
    if time == time_tot or time_step==(N_steps-1):
        print(':::SIMULATION FINISHED:::')
        print('writing results to file...')

        output = noninterp_outputs | interp_outputs #combine the two outputs
        output['grid'] = x #add the grid as well for easier plotting

        for key in output.keys():
            output[key] = np.array(output[key])

        np.savez_compressed(f'outputs/simulation_{PTtype}', **output)

        print('results file sucessfuly created...')
        print(':::PROCESS FINISHED:::')

        break


        
